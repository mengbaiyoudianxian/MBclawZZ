"""sub2api HTTP client — unified OpenAI-compatible entrypoint.

This client centralizes chat/completions and embeddings calls so the
mother runtime can treat sub2api as the single model-entry layer while
still keeping backward-compatible environment fallbacks.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx


class Sub2APIError(RuntimeError):
    """Raised when a sub2api request fails."""


@dataclass(slots=True)
class Sub2APIResult:
    """Normalized response wrapper for OpenAI-compatible calls."""

    raw: dict[str, Any]

    @property
    def content(self) -> str:
        choices = self.raw.get("choices") or []
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        return message.get("content", "")


def _resolve_base_url(base_url: str | None) -> str:
    candidate = (
        base_url
        or os.getenv("MBCLAW_SUB2API_BASE_URL")
        or os.getenv("MBCLAW_LLM_BASE_URL")
        or "http://127.0.0.1:8100/v1"
    )
    candidate = candidate.rstrip("/")
    if candidate.endswith("/v1"):
        return candidate
    return f"{candidate}/v1"


class Sub2APIClient:
    """Small OpenAI-compatible client used by the mother runtime.

    The client prefers the sub2api service but remains backwards compatible
    with direct OpenAI-compatible providers when the base URL points elsewhere.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        self.base_url = _resolve_base_url(base_url)
        self.api_key = (
            api_key
            if api_key is not None
            else os.getenv("MBCLAW_SUB2API_API_KEY")
            or os.getenv("MBCLAW_LLM_API_KEY", "")
        )
        self.model = model or os.getenv("MBCLAW_LLM_MODEL", "gpt-4o-mini")

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(self, path: str, body: dict[str, Any], timeout: float = 60.0) -> Sub2APIResult:
        try:
            response = httpx.post(
                f"{self.base_url}{path}",
                headers=self._headers(),
                json=body,
                timeout=timeout,
            )
            response.raise_for_status()
            return Sub2APIResult(raw=response.json())
        except Exception as exc:  # pragma: no cover - exercised through callers
            raise Sub2APIError(str(exc)) from exc

    def chat_completions(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        response_format: dict[str, Any] | None = None,
        extra_body: dict[str, Any] | None = None,
        timeout: float = 60.0,
    ) -> Sub2APIResult:
        body: dict[str, Any] = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format is not None:
            body["response_format"] = response_format
        if extra_body:
            body.update(extra_body)
        return self._request("/chat/completions", body, timeout=timeout)

    def chat(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        response_format: dict[str, Any] | None = None,
        extra_body: dict[str, Any] | None = None,
        timeout: float = 60.0,
    ) -> str:
        return self.chat_completions(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
            extra_body=extra_body,
            timeout=timeout,
        ).content

    def summarize_session(self, messages: list[dict], *, model: str | None = None, timeout: float = 60.0) -> dict[str, Any]:
        text = "\n".join(f"[{m.get('role', 'unknown')}]: {m.get('content', '')}" for m in messages)
        prompt = (
            "分析以下对话，严格输出 JSON：\n"
            '{"summary":"≤300字概括用户目标/达成结论/未决问题",'
            '"keywords":["最多10个"],'
            '"experiences":[{"kind":"success|failure|lesson","title":"≤80字","content":"≤500字"}]}\n'
            "experiences 最多 5 条。没有则空数组。\n"
            f"对话：\n{text}"
        )
        raw = self.chat(
            [{"role": "user", "content": prompt}],
            model=model,
            temperature=0.2,
            response_format={"type": "json_object"},
            timeout=timeout,
        )
        return json.loads(raw)

    def embeddings(self, text: str, *, model: str | None = None, timeout: float = 60.0) -> list[float] | None:
        try:
            result = self._request(
                "/embeddings",
                {
                    "model": model or os.getenv("MBCLAW_EMBED_MODEL", "text-embedding-3-small"),
                    "input": text[:8000],
                },
                timeout=timeout,
            )
        except Sub2APIError:
            return None
        data = result.raw.get("data") or []
        if not data:
            return None
        return data[0].get("embedding")

    def health(self, timeout: float = 5.0) -> dict[str, Any] | None:
        try:
            response = httpx.get(f"{self.base_url}/health", headers=self._headers(), timeout=timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


__all__ = ["Sub2APIClient", "Sub2APIError", "Sub2APIResult"]

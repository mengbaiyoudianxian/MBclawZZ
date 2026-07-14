"""T2.1 — LLM client for session summarisation.

Single-responsibility: call OpenAI-compatible /chat/completions,
parse the result into a validated LLMOutput.
"""

import json
import os

from pydantic import BaseModel, Field

from server_app.sub2api_client import Sub2APIClient


# ── exceptions ───────────────────────────────────────────────

class LLMError(Exception):
    """Raised when the LLM call fails after retries."""


# ── output model ─────────────────────────────────────────────

class _Experience(BaseModel):
    kind: str = Field(default="lesson")
    title: str = Field(max_length=80, default="")
    content: str = Field(max_length=500, default="")


class LLMOutput(BaseModel):
    summary: str = Field(max_length=400, default="")
    keywords: list[str] = Field(max_length=10, default_factory=list)
    experiences: list[_Experience] = Field(max_length=5, default_factory=list)


# ── prompt template (hardcoded, single) ──────────────────────

_SUMMARISE_PROMPT = """\
分析以下对话，严格输出 JSON：
{{
  "summary": "≤300字概括用户目标/达成结论/未决问题",
  "keywords": ["最多10个"],
  "experiences": [{{"kind":"success|failure|lesson","title":"≤80字","content":"≤500字"}}]
}}
experiences 最多 5 条。没有则空数组。
对话：
{messages_text}"""


# ── client ───────────────────────────────────────────────────

class LLMClient(Sub2APIClient):
    """Thin compatibility subclass for code that still imports LLMClient."""

    def summarize_session(self, messages: list[dict]) -> dict:
        if os.getenv("MBCLAW_LLM_MOCK") == "1":
            return {
                "summary": "[MOCK] 对话摘要。",
                "keywords": ["mock"],
                "experiences": [],
            }
        return super().summarize_session(messages, model=self.model, timeout=60)


__all__ = ["LLMClient", "LLMError", "get_llm", "LLMOutput"]


# ── DI helper ────────────────────────────────────────────────

def get_llm() -> LLMClient:
    """FastAPI dependency: return a default-configured LLMClient."""
    return LLMClient()

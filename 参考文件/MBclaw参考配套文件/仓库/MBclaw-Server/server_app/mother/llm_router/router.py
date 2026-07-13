from __future__ import annotations

import time
from typing import List

from .models import LLMRequest, LLMResponse
from .provider import Provider
from .token_pool import TokenPool
from .policy import ModelPolicyEngine


class LLMRouter:
    """
    Core LiteLLM-style routing system.
    """

    def __init__(self, providers: List[Provider], pool: TokenPool):
        self.providers = providers
        self.pool = pool
        self.policy = ModelPolicyEngine()

    def route(self, req: LLMRequest) -> LLMResponse:
        ranked = self.policy.rank(req, self.providers)

        for provider in ranked:
            estimated_cost = self._estimate_cost(req, provider)

            if not self.pool.is_available(provider.name, estimated_cost):
                continue

            start = time.time()

            try:
                output = provider.handler(req.prompt)

                latency = int((time.time() - start) * 1000)

                cost = estimated_cost
                self.pool.consume(provider.name, cost)

                return LLMResponse(
                    provider=provider.name,
                    model=provider.model,
                    output=output,
                    cost=cost,
                    latency_ms=latency,
                )

            except Exception:
                continue

        raise RuntimeError("No available provider satisfied constraints")

    def _estimate_cost(self, req: LLMRequest, provider: Provider) -> float:
        return (req.max_tokens / 1000) * provider.cost_per_1k_tokens

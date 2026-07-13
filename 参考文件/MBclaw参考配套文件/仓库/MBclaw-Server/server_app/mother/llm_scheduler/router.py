from __future__ import annotations

import time
from typing import List

from llm_router.models import LLMRequest, LLMResponse
from llm_router.provider import Provider
from llm_scheduler.strategy import ModelSchedulingStrategy
from llm_scheduler.token_pool import TokenPool


class Router:

    def __init__(self, providers: List[Provider], pool: TokenPool):
        self.providers = providers
        self.pool = pool
        self.strategy = ModelSchedulingStrategy()

    def route(self, req: LLMRequest) -> LLMResponse:

        ranked = self.strategy.rank(req, self.providers, self.pool)

        last_error = None

        for provider in ranked:

            estimated_cost = self._estimate(req, provider)

            # 1. token pool check
            if not self.pool.available(provider.name, estimated_cost):
                continue

            try:
                start = time.time()

                output = provider.handler(req.prompt)

                latency = int((time.time() - start) * 1000)

                # consume quota
                self.pool.providers[provider.name].remaining_quota -= estimated_cost

                return LLMResponse(
                    provider=provider.name,
                    model=provider.model,
                    output=output,
                    cost=estimated_cost,
                    latency_ms=latency,
                )

            except Exception as e:
                last_error = e
                continue

        raise RuntimeError(f"All providers failed: {last_error}")

    def _estimate(self, req: LLMRequest, provider: Provider) -> float:
        return (req.max_tokens / 1000) * provider.cost_per_1k_tokens

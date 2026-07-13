from __future__ import annotations

from typing import List
from llm_router.provider import Provider
from llm_router.models import LLMRequest
from llm_scheduler.token_pool import TokenPool


class ModelSchedulingStrategy:

    def score(self, req: LLMRequest, provider: Provider, pool: TokenPool) -> float:
        metrics = pool.get(provider.name)

        score = 0.0

        # cost factor
        score -= metrics.cost_per_1k * 2

        # latency factor
        score -= metrics.speed_ms / 1000

        # reliability factor
        score += metrics.success_rate * 3

        # budget constraint
        if req.budget < metrics.cost_per_1k:
            score -= 5

        # task type bias
        if req.task_type == "code" and "gpt" in provider.name:
            score += 2

        if req.task_type == "compress" and "small" in provider.name:
            score += 2

        if req.context_length > 8000:
            score += 1  # long context bias

        return score

    def rank(self, req: LLMRequest, providers: List[Provider], pool: TokenPool):
        return sorted(
            providers,
            key=lambda p: self.score(req, p, pool),
            reverse=True
        )

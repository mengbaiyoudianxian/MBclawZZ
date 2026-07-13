from __future__ import annotations

from typing import List

from .models import LLMRequest
from .provider import Provider


class ModelPolicyEngine:
    """
    Chooses best model based on task type + constraints.
    """

    def score(self, req: LLMRequest, provider: Provider) -> float:
        score = 0.0

        # cost sensitivity
        score -= provider.cost_per_1k_tokens * 2

        # latency sensitivity
        score -= provider.avg_latency_ms / 1000

        # success rate bonus
        score += provider.success_rate * 2

        # task-specific heuristics
        if req.task_type == "code" and "gpt" in provider.name:
            score += 2

        if req.task_type == "compress" and "small" in provider.name:
            score += 2

        if req.priority > 5:
            score += 1

        return score

    def rank(self, req: LLMRequest, providers: List[Provider]):
        return sorted(
            providers,
            key=lambda p: self.score(req, p),
            reverse=True,
        )

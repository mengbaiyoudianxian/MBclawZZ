from __future__ import annotations

import time
from typing import Optional

from llm_token_pool.registry import ProviderRegistry
from llm_token_pool.metrics import MetricsStore, CallStat
from llm_token_pool.circuit import CircuitBreaker


class TokenPool:
    """
    Unified LLM resource manager:
    - API keys
    - cost tracking
    - metrics
    - circuit breaker
    """

    def __init__(self, registry: ProviderRegistry):
        self.registry = registry

        self.metrics = MetricsStore()
        self.circuit = CircuitBreaker()

        # quota tracking
        self.quota_used = {}

    # --------------------------
    # provider selection support
    # --------------------------

    def available(self, provider: str) -> bool:
        return self.circuit.allow(provider)

    def mark_success(self, provider: str, latency_ms: float):
        self.metrics.record(provider, CallStat(
            latency_ms=latency_ms,
            success=True
        ))
        self.circuit.record_success(provider)

    def mark_failure(self, provider: str, error_code: str = "unknown"):
        self.metrics.record(provider, CallStat(
            latency_ms=0,
            success=False,
            error_code=error_code
        ))
        self.circuit.record_failure(provider)

    # --------------------------
    # cost / quota
    # --------------------------

    def consume(self, provider: str, cost: float):
        self.quota_used[provider] = self.quota_used.get(provider, 0) + cost

    def remaining(self, provider: str) -> float:
        p = self.registry.get(provider)
        used = self.quota_used.get(provider, 0)
        return max(0, 100 - used)  # assume default quota=100

    # --------------------------
    # analytics
    # --------------------------

    def stats(self, provider: str):
        return {
            "success_rate": self.metrics.success_rate(provider),
            "avg_latency": self.metrics.avg_latency(provider),
            "error_rate": self.metrics.error_rate(provider),
            "remaining_quota": self.remaining(provider),
        }

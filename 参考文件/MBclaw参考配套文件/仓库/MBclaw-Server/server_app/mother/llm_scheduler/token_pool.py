from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ProviderMetrics:
    speed_ms: float
    cost_per_1k: float
    success_rate: float
    remaining_quota: float


class TokenPool:
    """
    Real-time provider resource tracker
    """

    def __init__(self):
        self.providers: Dict[str, ProviderMetrics] = {}

    def update(self, name: str, metrics: ProviderMetrics):
        self.providers[name] = metrics

    def get(self, name: str) -> ProviderMetrics:
        return self.providers[name]

    def available(self, name: str, estimated_cost: float) -> bool:
        p = self.providers.get(name)
        if not p:
            return False
        return p.remaining_quota >= estimated_cost

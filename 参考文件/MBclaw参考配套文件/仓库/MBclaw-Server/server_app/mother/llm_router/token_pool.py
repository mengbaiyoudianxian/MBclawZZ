from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TokenPool:
    """
    Tracks provider quota + budget availability.
    """

    quota: Dict[str, float] = field(default_factory=dict)
    usage: Dict[str, float] = field(default_factory=dict)

    def remaining(self, provider: str) -> float:
        return self.quota.get(provider, 0) - self.usage.get(provider, 0)

    def consume(self, provider: str, cost: float):
        self.usage[provider] = self.usage.get(provider, 0) + cost

    def is_available(self, provider: str, cost: float) -> bool:
        return self.remaining(provider) >= cost

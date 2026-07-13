from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Metrics:
    """
    Lightweight runtime metrics collector.
    """

    counters: Dict[str, int] = field(default_factory=dict)

    def inc(self, key: str, value: int = 1):
        self.counters[key] = self.counters.get(key, 0) + value

    def get(self, key: str) -> int:
        return self.counters.get(key, 0)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
import time


@dataclass
class CallStat:
    latency_ms: float
    success: bool
    error_code: str | None = None


class MetricsStore:
    """
    Tracks provider performance in real-time.
    """

    def __init__(self):
        self.stats: Dict[str, list[CallStat]] = {}

    def record(self, provider: str, stat: CallStat):
        self.stats.setdefault(provider, []).append(stat)

    def success_rate(self, provider: str) -> float:
        s = self.stats.get(provider, [])
        if not s:
            return 1.0
        return sum(1 for x in s if x.success) / len(s)

    def avg_latency(self, provider: str) -> float:
        s = self.stats.get(provider, [])
        if not s:
            return 0.0
        return sum(x.latency_ms for x in s) / len(s)

    def error_rate(self, provider: str) -> float:
        s = self.stats.get(provider, [])
        if not s:
            return 0.0
        return sum(1 for x in s if not x.success) / len(s)

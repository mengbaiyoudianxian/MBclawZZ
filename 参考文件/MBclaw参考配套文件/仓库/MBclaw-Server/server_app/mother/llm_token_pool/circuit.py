from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import time


@dataclass
class CircuitState:
    failures: int = 0
    last_fail_time: float = 0.0
    open: bool = False


class CircuitBreaker:
    """
    Provider-level circuit breaker.
    """

    def __init__(self, threshold: int = 3, cooldown: float = 30):
        self.threshold = threshold
        self.cooldown = cooldown
        self.states: Dict[str, CircuitState] = {}

    def allow(self, provider: str) -> bool:
        state = self.states.get(provider)
        if not state:
            return True

        if not state.open:
            return True

        # cooldown check
        if time.time() - state.last_fail_time > self.cooldown:
            state.open = False
            state.failures = 0
            return True

        return False

    def record_success(self, provider: str):
        self.states.pop(provider, None)

    def record_failure(self, provider: str):
        state = self.states.setdefault(provider, CircuitState())

        state.failures += 1
        state.last_fail_time = time.time()

        if state.failures >= self.threshold:
            state.open = True

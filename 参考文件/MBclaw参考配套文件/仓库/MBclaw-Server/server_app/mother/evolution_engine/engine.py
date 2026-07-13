from __future__ import annotations

from typing import Dict

from evolution_engine.analyzer import SignalAnalyzer
from evolution_engine.policy_mutator import PolicyMutator

from memory_engine_v2.memory_engine import MemoryEngineV2


class EvolutionEngine:

    def __init__(self, memory: MemoryEngineV2):
        self.memory = memory

        self.analyzer = SignalAnalyzer()
        self.mutator = PolicyMutator()

        # current runtime policy
        self.runtime_policy: Dict = {
            "importance_boost": 0.1,
            "failure_penalty": 0.1,
            "compression_threshold": 0.85,
            "retrieval_bias": 1.0
        }

    # -------------------------
    # main evolution loop
    # -------------------------

    def evolve(self):

        memories = self.memory.store.all()

        signals = self.analyzer.extract(memories)

        new_policy = self.mutator.mutate_memory_policy(signals)

        self._apply(new_policy)

        return self.runtime_policy

    # -------------------------
    # apply policy update
    # -------------------------

    def _apply(self, delta: Dict):

        self.runtime_policy["importance_boost"] += delta["importance_boost"]
        self.runtime_policy["failure_penalty"] += delta["failure_penalty"]

        self.runtime_policy["compression_threshold"] += delta["compression_threshold_shift"]

        self.runtime_policy["retrieval_bias"] += delta["retrieval_bias"]

        # clamp
        self.runtime_policy["compression_threshold"] = max(
            0.5,
            min(0.95, self.runtime_policy["compression_threshold"])
        )

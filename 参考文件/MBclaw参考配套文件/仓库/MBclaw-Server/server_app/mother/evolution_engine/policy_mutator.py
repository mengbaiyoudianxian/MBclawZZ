from __future__ import annotations

from typing import Dict
from evolution_engine.signals import EvolutionSignal


class PolicyMutator:

    def mutate_memory_policy(self, signals: list[EvolutionSignal]) -> Dict:

        policy = {
            "importance_boost": 0.0,
            "failure_penalty": 0.0,
            "compression_threshold_shift": 0.0,
            "retrieval_bias": 0.0
        }

        for s in signals:

            if s.type == "success":
                policy["importance_boost"] += 0.02 * s.weight

            if s.type == "failure":
                policy["failure_penalty"] += 0.03 * s.weight

            if s.type == "repetition":
                policy["retrieval_bias"] += 0.05

            if s.type == "efficiency":
                policy["compression_threshold_shift"] -= 0.02

        return policy

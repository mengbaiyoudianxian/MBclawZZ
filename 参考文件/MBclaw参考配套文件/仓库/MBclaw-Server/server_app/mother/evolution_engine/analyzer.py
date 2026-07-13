from __future__ import annotations

from typing import List, Dict


class EvolutionAnalyzer:

    def analyze_audit(self, audit_events: List[dict]):

        failures = []
        slow_calls = []
        expensive_calls = []

        for e in audit_events:

            if not e.get("success"):
                failures.append(e)

            if e.get("latency_ms", 0) > 2000:
                slow_calls.append(e)

            if e.get("token_cost", 0) > 1000:
                expensive_calls.append(e)

        return {
            "failures": failures,
            "slow": slow_calls,
            "expensive": expensive_calls
        }

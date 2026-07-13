from __future__ import annotations


class EvolutionOptimizer:

    def prioritize(self, prts: list):

        def score(p):

            if p["type"] == "workflow_restructure":
                return 3
            if p["type"] == "scheduler_adjustment":
                return 2
            return 1

        return sorted(prts, key=score, reverse=True)

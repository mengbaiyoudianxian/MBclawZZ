from __future__ import annotations

from collections import defaultdict


class FailurePatternDetector:

    def detect(self, analysis: dict):

        patterns = defaultdict(int)

        for f in analysis["failures"]:

            key = f.get("target", "unknown")

            patterns[key] += 1

        return {
            "repeated_failures": [
                {"target": k, "count": v}
                for k, v in patterns.items()
                if v >= 3
            ]
        }

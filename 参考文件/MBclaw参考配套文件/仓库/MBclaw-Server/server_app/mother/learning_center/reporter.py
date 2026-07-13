from __future__ import annotations


class LearningReporter:

    def generate_report(self, items: list):

        report = {
            "new_knowledge": len(items),
            "categories": {},
            "suggestions": []
        }

        for i in items:

            t = i.get("type")

            report["categories"][t] = report["categories"].get(t, 0) + 1

        # -----------------------------
        # auto strategy suggestions
        # -----------------------------

        if report["categories"].get("architecture", 0) > 0:

            report["suggestions"].append(
                "Consider updating Scheduler routing strategy"
            )

        if report["categories"].get("bug", 0) > 0:

            report["suggestions"].append(
                "Increase Governor strictness level"
            )

        return report

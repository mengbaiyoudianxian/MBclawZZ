from __future__ import annotations


class CognitiveClassifier:

    def classify(self, text: str) -> str:

        t = text.lower()

        # project 1: raw record
        if "log" in t or "chat" in t:
            return "dialogue"

        # tool system (project 11)
        if "tool" in t or "skill" in t:
            return "capability"

        # failure case (project 2)
        if "not work" in t or "fail" in t:
            return "failure_case"

        # success case
        if "success" in t or "ok" in t:
            return "success_case"

        # vision interaction
        if "click" in t or "screen" in t:
            return "vision_action"

        return "general"

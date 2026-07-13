from __future__ import annotations

from typing import List


class KnowledgeExtractor:

    # -----------------------------
    # text -> structured knowledge
    # -----------------------------

    def extract(self, item: dict) -> dict:

        content = item.get("content", "")

        return {
            "type": self._classify(content),
            "summary": content[:200],
            "tags": self._tag(content),
            "confidence": 0.7
        }

    def _classify(self, text: str):

        if "bug" in text:
            return "bug"
        if "router" in text:
            return "architecture"
        return "general"

    def _tag(self, text: str):

        tags = []

        if "router" in text:
            tags.append("scheduler")
        if "performance" in text:
            tags.append("optimization")

        return tags

from __future__ import annotations

from packaging import version
from typing import List


class VersionManager:

    def is_compatible(self, v1: str, v2: str) -> bool:
        return version.parse(v1) >= version.parse(v2)

    def resolve(self, capabilities: List[dict]):
        """
        resolve compatibility conflicts
        """
        sorted_caps = sorted(
            capabilities,
            key=lambda x: version.parse(x["version"].version),
            reverse=True
        )

        resolved = {}

        for cap in sorted_caps:
            name = cap["name"]
            if name not in resolved:
                resolved[name] = cap

        return list(resolved.values())

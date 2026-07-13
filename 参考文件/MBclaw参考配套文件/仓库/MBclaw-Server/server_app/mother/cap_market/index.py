from __future__ import annotations

from typing import List

from cap_market.registry import CapRegistry
from cap_market.cap_format import CapPackage


class CapIndex:

    def __init__(self, registry: CapRegistry):
        self.registry = registry

    # -----------------------
    # search
    # -----------------------

    def search(self, keyword: str) -> List[CapPackage]:
        result = []

        for caps in self.registry.store.values():
            for c in caps:
                if keyword.lower() in c.name.lower() or keyword.lower() in c.description.lower():
                    result.append(c)

        return result

    # -----------------------
    # category (simple metadata-based)
    # -----------------------

    def by_type(self, cap_type: str) -> List[CapPackage]:
        result = []

        for caps in self.registry.store.values():
            for c in caps:
                if c.metadata.get("type") == cap_type:
                    result.append(c)

        return result

    # -----------------------
    # pull
    # -----------------------

    def fetch(self, name: str) -> CapPackage | None:
        return self.registry.get_latest(name)

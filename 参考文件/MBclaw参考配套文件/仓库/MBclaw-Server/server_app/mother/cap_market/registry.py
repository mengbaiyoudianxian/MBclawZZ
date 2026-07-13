from __future__ import annotations

from typing import Dict, List, Optional
from cap_market.cap_format import CapPackage


class CapRegistry:
    """
    marketplace registry (search + store + rating)
    """

    def __init__(self):
        self.store: Dict[str, List[CapPackage]] = {}
        self.ratings: Dict[str, float] = {}

    # -----------------------
    # publish
    # -----------------------

    def publish(self, cap: CapPackage):
        self.store.setdefault(cap.name, []).append(cap)

    # -----------------------
    # query
    # -----------------------

    def get_latest(self, name: str) -> Optional[CapPackage]:
        caps = self.store.get(name)
        if not caps:
            return None

        return sorted(caps, key=lambda c: c.version, reverse=True)[0]

    def list_all(self):
        return [
            self.get_latest(name)
            for name in self.store.keys()
        ]

    # -----------------------
    # rating system
    # -----------------------

    def rate(self, name: str, score: float):
        self.ratings[name] = (self.ratings.get(name, 0) + score) / 2

    def get_rating(self, name: str) -> float:
        return self.ratings.get(name, 0.0)

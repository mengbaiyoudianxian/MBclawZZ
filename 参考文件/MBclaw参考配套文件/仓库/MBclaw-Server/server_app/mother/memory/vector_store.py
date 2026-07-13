from __future__ import annotations

from typing import Dict, List, Any
import math


class VectorStore:
    """
    Minimal vector memory abstraction (no external dependency).
    """

    def __init__(self):
        self.store: Dict[str, List[float]] = {}
        self.meta: Dict[str, Any] = {}

    def add(self, key: str, vector: List[float], metadata: Any = None):
        self.store[key] = vector
        self.meta[key] = metadata

    def cosine(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        return dot / (na * nb + 1e-9)

    def search(self, query_vec: List[float], top_k: int = 5):
        scored = []

        for k, v in self.store.items():
            scored.append((self.cosine(query_vec, v), k))

        scored.sort(reverse=True)

        return scored[:top_k]

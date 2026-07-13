from __future__ import annotations

import math
from typing import List
from memory_engine.memory import MemoryItem


class VectorStore:

    def __init__(self):
        self.items: List[MemoryItem] = []

    def add(self, item: MemoryItem):
        self.items.append(item)

    # cosine similarity
    def _sim(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        return dot / (na * nb + 1e-8)

    def search(self, query_embedding: List[float], top_k: int = 5):

        scored = []

        for item in self.items:
            score = self._sim(query_embedding, item.embedding)
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [i for _, i in scored[:top_k]]

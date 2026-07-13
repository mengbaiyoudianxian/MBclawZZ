from __future__ import annotations

import math
from typing import List
from memory_engine_v2.memory_schema import MemoryRecord


class SemanticEngine:

    def cosine(self, a: List[float], b: List[float]) -> float:
        dot = sum(x*y for x, y in zip(a, b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        return dot / (na * nb + 1e-9)

    def search(self, query_vec: List[float], pool: List[MemoryRecord], top_k=8):

        scored = []

        for r in pool:
            if not r.embedding:
                continue
            score = self.cosine(query_vec, r.embedding)

            # fuse importance (project 14)
            score *= (1 + r.importance)

            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [r for _, r in scored[:top_k]]

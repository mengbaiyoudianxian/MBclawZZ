from __future__ import annotations

from typing import List

from memory_engine.vector_store import VectorStore
from memory_engine.memory import MemoryItem
from memory_engine.importance import ImportanceModel


class MemoryRetriever:

    def __init__(self, store: VectorStore):
        self.store = store
        self.importance_model = ImportanceModel()

    def retrieve(self, query_embedding: List[float], top_k: int = 5):

        results = self.store.search(query_embedding, top_k * 2)

        # rerank with importance
        ranked = sorted(
            results,
            key=lambda x: x.importance,
            reverse=True
        )

        for item in ranked[:top_k]:
            self.importance_model.update_on_access(item)

        return ranked[:top_k]

    def reinforce(self, item: MemoryItem):
        self.importance_model.update_on_access(item)

    def decay(self):
        self.importance_model.decay_all(self.store.items)

from __future__ import annotations

import uuid
from typing import List

from memory_engine.memory import MemoryItem
from memory_engine.vector_store import VectorStore
from memory_engine.retriever import MemoryRetriever


class MemoryEngine:

    def __init__(self):
        self.store = VectorStore()
        self.retriever = MemoryRetriever(self.store)

    # -------------------------
    # write memory
    # -------------------------

    def write(self, content: str, embedding: List[float], tags: List[str] = None):

        item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            embedding=embedding,
            tags=tags or []
        )

        self.store.add(item)

        return item.id

    # -------------------------
    # semantic recall
    # -------------------------

    def recall(self, query_embedding: List[float], top_k: int = 5):

        return self.retriever.retrieve(query_embedding, top_k)

    # -------------------------
    # reinforce memory
    # -------------------------

    def reinforce(self, memory_id: str):

        for item in self.store.items:
            if item.id == memory_id:
                self.retriever.reinforce(item)

    # -------------------------
    # periodic decay
    # -------------------------

    def decay_cycle(self):
        self.retriever.decay()

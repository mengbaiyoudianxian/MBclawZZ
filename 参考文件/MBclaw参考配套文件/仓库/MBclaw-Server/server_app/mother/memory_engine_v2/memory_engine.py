from __future__ import annotations

import uuid
from typing import List

from memory_engine_v2.memory_schema import MemoryRecord
from memory_engine_v2.memory_store import MemoryStore
from memory_engine_v2.semantic_engine import SemanticEngine
from memory_engine_v2.importance_system import ImportanceSystem
from memory_engine_v2.cognitive_classifier import CognitiveClassifier


class MemoryEngineV2:

    def __init__(self):
        self.store = MemoryStore()
        self.semantic = SemanticEngine()
        self.importance = ImportanceSystem()
        self.classifier = CognitiveClassifier()

    # -----------------------------
    # write (project 1 core)
    # -----------------------------

    def write(self, raw: str, embedding: List[float], keywords=None):

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            raw=raw,
            embedding=embedding,
            keywords=keywords or [],
            category=self.classifier.classify(raw),
        )

        self.store.write(record)

        return record.id

    # -----------------------------
    # semantic recall (project 2/6)
    # -----------------------------

    def recall(self, query_vec: List[float]) -> List[MemoryRecord]:

        return self.semantic.search(
            query_vec,
            self.store.all()
        )

    # -----------------------------
    # success reinforcement (project 14)
    # -----------------------------

    def mark_success(self, mid: str):

        r = self.store.get(mid)
        if r:
            self.importance.reinforce_success(r)

    # -----------------------------
    # failure punishment (project 2)
    # -----------------------------

    def mark_failure(self, mid: str):

        r = self.store.get(mid)
        if r:
            self.importance.punish_failure(r)

    # -----------------------------
    # periodic decay (long-term memory control)
    # -----------------------------

    def decay_cycle(self):

        for r in self.store.all():
            self.importance.decay(r)

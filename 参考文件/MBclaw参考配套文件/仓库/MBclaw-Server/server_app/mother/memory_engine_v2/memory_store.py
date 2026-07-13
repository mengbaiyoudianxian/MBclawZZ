from __future__ import annotations

from typing import List, Dict
from memory_engine_v2.memory_schema import MemoryRecord


class MemoryStore:

    def __init__(self):
        self.raw_store: List[MemoryRecord] = []     # permanent raw records (project 1)
        self.index: Dict[str, MemoryRecord] = {}    # fast lookup index

    def write(self, record: MemoryRecord):
        self.raw_store.append(record)
        self.index[record.id] = record

    def get(self, mid: str):
        return self.index.get(mid)

    def all(self):
        return self.raw_store

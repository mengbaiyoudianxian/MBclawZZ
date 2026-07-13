from __future__ import annotations

from memory_engine_v2.memory_schema import MemoryRecord


class ImportanceSystem:

    def reinforce_success(self, record: MemoryRecord):

        record.importance = min(1.0, record.importance + 0.15)
        record.success = True
        record.access_count += 1

    def punish_failure(self, record: MemoryRecord):

        record.importance = max(0.05, record.importance - 0.2)
        record.success = False

    def decay(self, record: MemoryRecord):

        record.importance *= 0.995

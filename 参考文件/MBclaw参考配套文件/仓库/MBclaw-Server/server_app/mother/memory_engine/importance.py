from __future__ import annotations

from memory_engine.memory import MemoryItem


class ImportanceModel:

    def update_on_access(self, item: MemoryItem):
        item.access_count += 1
        item.last_accessed = item.created_at

        # reinforce importance
        item.importance = min(
            1.0,
            item.importance + 0.05
        )

    def decay_all(self, items: list[MemoryItem]):
        for item in items:
            time_decay = item.decay

            item.importance *= time_decay

            # floor threshold
            if item.importance < 0.05:
                item.importance = 0.05

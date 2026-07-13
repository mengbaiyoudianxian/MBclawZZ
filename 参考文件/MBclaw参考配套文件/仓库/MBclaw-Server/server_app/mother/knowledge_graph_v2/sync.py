from __future__ import annotations

from knowledge_graph_v2.entity import KGEntity


class MemoryGraphBridge:

    # Memory -> Graph (dual-write entry)

    def memory_to_entity(self, m) -> KGEntity:

        return KGEntity(
            id=m.id,
            type=getattr(m, "layer", getattr(m, "category", "memory")),
            name=getattr(m, "layer", getattr(m, "category", "memory")),
            content=getattr(m, "content", getattr(m, "raw", "")),
            meta=getattr(m, "meta", {}),
            importance=getattr(m, "importance", 0.5)
        )

    # Graph -> Memory (reverse write-back)

    def entity_to_memory(self, e: KGEntity):

        from memory_engine_v2.memory_schema import MemoryRecord

        return MemoryRecord(
            id=e.id,
            raw=e.content,
            category=e.type,
            importance=e.importance,
            keywords=[e.name],
        )

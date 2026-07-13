from __future__ import annotations

from knowledge_graph.entity import KGNode


class GraphImporter:

    def memory_to_graph(self, memory) -> KGNode:

        return KGNode(
            id=memory.id,
            type=getattr(memory, "layer", "memory"),
            name=getattr(memory, "layer", "memory"),
            content=getattr(memory, "content", getattr(memory, "raw", "")),
            meta=getattr(memory, "meta", {}),
            importance=getattr(memory, "importance", 0.5)
        )

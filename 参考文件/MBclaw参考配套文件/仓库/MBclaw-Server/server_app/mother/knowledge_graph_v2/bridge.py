from __future__ import annotations

from knowledge_graph_v2.graph import KnowledgeGraphV2
from knowledge_graph_v2.sync import MemoryGraphBridge


class KnowledgeBrainBridge:

    def __init__(self, graph: KnowledgeGraphV2):

        self.graph = graph
        self.bridge = MemoryGraphBridge()

    # -------------------------
    # Memory -> KG (ingest)
    # -------------------------

    def ingest_memory(self, memory):

        entity = self.bridge.memory_to_entity(memory)

        self.graph.add_entity(entity)

    # -------------------------
    # KG -> Memory (export back)
    # -------------------------

    def export_memory(self, entity_id: str):

        entity = self.graph.get(entity_id)

        if not entity:
            return None

        return self.bridge.entity_to_memory(entity)

    # -------------------------
    # graph reasoning acceleration (core)
    # -------------------------

    def fast_trace(self, node_id: str):

        return self.graph.expand(node_id)

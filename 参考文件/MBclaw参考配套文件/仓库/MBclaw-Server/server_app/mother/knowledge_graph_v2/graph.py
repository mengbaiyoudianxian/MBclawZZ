from __future__ import annotations

from typing import Dict, List
from knowledge_graph_v2.entity import KGEntity
from knowledge_graph_v2.edge import KGRelation


class KnowledgeGraphV2:

    def __init__(self):

        self.nodes: Dict[str, KGEntity] = {}
        self.edges: List[KGRelation] = []

    # -------------------------
    # node write (dynamic growth)
    # -------------------------

    def add_entity(self, node: KGEntity):
        self.nodes[node.id] = node

    # -------------------------
    # edge write
    # -------------------------

    def add_relation(self, edge: KGRelation):
        self.edges.append(edge)

    # -------------------------
    # query node
    # -------------------------

    def get(self, node_id: str):
        return self.nodes.get(node_id)

    # -------------------------
    # adjacency expansion (reasoning foundation)
    # -------------------------

    def expand(self, node_id: str):

        return [
            e for e in self.edges
            if e.source == node_id or e.target == node_id
        ]

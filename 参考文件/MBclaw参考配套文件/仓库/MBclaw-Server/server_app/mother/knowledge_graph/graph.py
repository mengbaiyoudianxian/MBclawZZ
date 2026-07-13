from __future__ import annotations

from typing import Dict, List
from knowledge_graph.entity import KGNode
from knowledge_graph.edge import KGEdge


class KnowledgeGraph:

    def __init__(self):

        self.nodes: Dict[str, KGNode] = {}
        self.edges: List[KGEdge] = []

    # -----------------------------
    # add node
    # -----------------------------

    def add_node(self, node: KGNode):

        self.nodes[node.id] = node

    # -----------------------------
    # add edge
    # -----------------------------

    def add_edge(self, edge: KGEdge):

        self.edges.append(edge)

    # -----------------------------
    # query node
    # -----------------------------

    def get(self, node_id: str):
        return self.nodes.get(node_id)

    # -----------------------------
    # adjacency query
    # -----------------------------

    def neighbors(self, node_id: str):

        return [
            e for e in self.edges
            if e.source == node_id or e.target == node_id
        ]

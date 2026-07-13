from __future__ import annotations

from memory_federation.merge_engine import GraphMergeEngine


class FederationServer:

    def __init__(self, merge_engine: GraphMergeEngine = None):

        self.merge_engine = merge_engine or GraphMergeEngine()

        self.global_graph = {
            "nodes": [],
            "edges": [],
            "meta": {}
        }

    def ingest(self, packet):

        incoming = {
            "nodes": packet.graph_nodes,
            "edges": packet.graph_edges,
            "meta": packet.vector_meta
        }

        self.global_graph = self.merge_engine.merge(
            self.global_graph,
            incoming
        )

        return self.global_graph

from __future__ import annotations

from typing import Dict

from memory_federation.sync_protocol import SyncProtocol
from memory_federation.node import FederationNode


class FederationClient:

    def __init__(self, node_id: str, graph_engine):

        self.node = FederationNode(node_id=node_id, device_type="edge")
        self.protocol = SyncProtocol()
        self.graph_engine = graph_engine

        self.buffer = []

    # -----------------------------
    # push local memory
    # -----------------------------

    def push(self):

        local_graph = self.graph_engine.export_graph()

        packet = self.protocol.encode(local_graph, self.node.node_id)

        return packet

    # -----------------------------
    # receive mother update
    # -----------------------------

    def pull(self, packet):

        if not self.protocol.validate(packet, self.node):
            return False

        merged = {
            "nodes": packet.graph_nodes,
            "edges": packet.graph_edges,
            "meta": packet.vector_meta
        }

        self.graph_engine.import_graph(merged)

        return True

from __future__ import annotations

from memory_federation.packet import MemoryPacket
from memory_federation.node import FederationNode


class SyncProtocol:

    def encode(self, local_graph, node_id: str) -> MemoryPacket:

        return MemoryPacket(
            sender_id=node_id,
            graph_nodes=local_graph.get("nodes", []),
            graph_edges=local_graph.get("edges", []),
            vector_meta=local_graph.get("meta", {})
        )

    def validate(self, packet: MemoryPacket, node: FederationNode) -> bool:

        # trust gating (anti-pollution)
        if node.trust_score < 0.3:
            return False

        if len(packet.graph_nodes) > 10000:
            return False

        return True

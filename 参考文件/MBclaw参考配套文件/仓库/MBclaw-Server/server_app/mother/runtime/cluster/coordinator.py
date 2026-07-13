from __future__ import annotations

from typing import List, Dict, Any

from .node import WorkerNode
from .load_balancer import LoadBalancer


class ClusterCoordinator:
    """
    Manages distributed execution nodes.
    """

    def __init__(self):
        self.nodes: List[WorkerNode] = []
        self.lb = LoadBalancer()

    def register_node(self, node: WorkerNode):
        self.nodes.append(node)

    def assign_task(self, task: Dict[str, Any]) -> WorkerNode | None:
        node = self.lb.select_node(self.nodes)

        if node:
            node.load += 1

        return node

    def release_task(self, node: WorkerNode):
        node.load = max(0, node.load - 1)

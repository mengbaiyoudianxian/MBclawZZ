from __future__ import annotations

from typing import List, Optional

from .node import WorkerNode


class LoadBalancer:
    """
    Simple least-loaded scheduler for distributed workers.
    """

    def select_node(self, nodes: List[WorkerNode]) -> Optional[WorkerNode]:
        available = [n for n in nodes if n.is_available()]

        if not available:
            return None

        return sorted(available, key=lambda n: n.load)[0]

from __future__ import annotations

import time
from typing import List

from .node import WorkerNode


class HeartbeatMonitor:
    """
    Detects node failure / offline status.
    """

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def check(self, nodes: List[WorkerNode]) -> List[WorkerNode]:
        now = time.time()

        alive = []
        for n in nodes:
            if now - n.last_heartbeat <= self.timeout:
                alive.append(n)

        return alive

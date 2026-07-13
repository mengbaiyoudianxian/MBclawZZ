from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import time


@dataclass
class WorkerNode:
    node_id: str
    capacity: int = 10
    load: int = 0
    last_heartbeat: float = 0.0

    def is_available(self) -> bool:
        return self.load < self.capacity

    def heartbeat(self):
        self.last_heartbeat = time.time()

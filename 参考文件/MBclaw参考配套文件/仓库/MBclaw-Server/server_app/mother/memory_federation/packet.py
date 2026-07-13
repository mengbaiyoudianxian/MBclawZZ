from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any
import time


@dataclass
class MemoryPacket:

    sender_id: str

    graph_nodes: List[Dict]

    graph_edges: List[Dict]

    vector_meta: Dict[str, Any]

    timestamp: float = field(default_factory=lambda: time.time())

    signature: str = ""

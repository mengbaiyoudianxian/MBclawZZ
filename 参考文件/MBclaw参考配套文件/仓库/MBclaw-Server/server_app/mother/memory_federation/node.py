from __future__ import annotations

from dataclasses import dataclass
import time


@dataclass
class FederationNode:

    node_id: str
    device_type: str  # mobile / server / edge

    trust_score: float = 0.5

    last_seen: float = time.time()

    version: int = 1

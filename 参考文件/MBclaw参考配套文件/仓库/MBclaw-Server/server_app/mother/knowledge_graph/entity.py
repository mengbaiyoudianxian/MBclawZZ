from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class KGNode:

    id: str

    type: str
    # module / bug / fix / tool / decision / doc / memory

    name: str

    content: str

    meta: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=lambda: time.time())

    importance: float = 0.5

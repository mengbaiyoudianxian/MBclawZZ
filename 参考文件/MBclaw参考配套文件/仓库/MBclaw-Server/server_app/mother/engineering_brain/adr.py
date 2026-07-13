from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class ADR:

    id: str

    title: str

    context: str

    decision: str

    consequences: str

    status: str  # accepted / deprecated / superseded

    meta: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=lambda: time.time())

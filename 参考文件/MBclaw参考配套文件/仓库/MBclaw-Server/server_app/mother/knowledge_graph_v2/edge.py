from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class KGRelation:

    source: str
    target: str

    relation: str
    # fixes / depends_on / causes / references / improves / conflicts_with

    weight: float = 1.0

    meta: Dict[str, Any] = field(default_factory=dict)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class EngineeringKnowledge:

    id: str

    type: str
    # bug / fix / pattern / anti_pattern / rule / guideline

    title: str

    content: str

    confidence: float = 0.5

    tags: list = field(default_factory=list)

    meta: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=lambda: time.time())

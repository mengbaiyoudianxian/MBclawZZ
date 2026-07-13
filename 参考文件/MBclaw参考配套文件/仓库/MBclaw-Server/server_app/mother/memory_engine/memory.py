from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List
import time


@dataclass
class MemoryItem:
    id: str
    content: str

    embedding: List[float]

    importance: float = 0.5
    decay: float = 0.99

    tags: List[str] = field(default_factory=list)

    created_at: float = field(default_factory=lambda: time.time())

    last_accessed: float = field(default_factory=lambda: time.time())

    access_count: int = 0

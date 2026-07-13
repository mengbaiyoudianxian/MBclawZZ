from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class TaskNode:

    id: str

    task: str

    agent_hint: str = ""

    dependencies: List[str] = field(default_factory=list)

    status: str = "pending"

    result: Any = None

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


def _id():
    return str(uuid4())


@dataclass
class Task:
    task_id: str = field(default_factory=_id)

    name: str = ""
    description: str = ""

    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)

    dependencies: List[str] = field(default_factory=list)

    required_capabilities: List[str] = field(default_factory=list)

    estimated_cost: float = 1.0
    priority: int = 0

    status: str = "pending"


@dataclass
class Plan:
    plan_id: str = field(default_factory=_id)

    goal: str = ""

    tasks: List[Task] = field(default_factory=list)

    context: Dict[str, Any] = field(default_factory=dict)

    version: int = 1

    status: str = "created"

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Message:
    role: str  # user / assistant / system
    content: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkspaceState:
    todo: List[str] = field(default_factory=list)
    code_diff: List[str] = field(default_factory=list)
    key_artifacts: List[str] = field(default_factory=list)


@dataclass
class ContextBundle:
    raw_messages: List[Message]
    workspace: WorkspaceState
    memory_refs: List[str] = field(default_factory=list)

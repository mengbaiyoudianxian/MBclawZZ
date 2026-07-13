from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List
import time


@dataclass
class MemoryRecord:

    id: str

    # raw content (project 1 core)
    raw: str

    # structured summary (project 2)
    summary: Dict[str, Any] = field(default_factory=dict)

    # tags / keywords
    keywords: List[str] = field(default_factory=list)

    # category (dialogue/tool/skill/failure_case/success_case)
    category: str = "dialogue"

    # vector representation
    embedding: List[float] = field(default_factory=list)

    # importance score (project 14/16)
    importance: float = 0.5

    # success/failure marker
    success: bool | None = None

    # source type (skill/tool/chat/vision/system)
    source: str = "chat"

    # subtask references (project 10)
    task_refs: List[str] = field(default_factory=list)

    created_at: float = field(default_factory=lambda: time.time())
    last_access: float = field(default_factory=lambda: time.time())

    access_count: int = 0

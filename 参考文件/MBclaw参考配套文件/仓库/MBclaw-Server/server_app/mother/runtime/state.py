from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class RuntimeStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class RuntimeState:
    """
    Global runtime state for MBclaw execution kernel.
    """

    status: RuntimeStatus = RuntimeStatus.IDLE

    current_task_id: Optional[str] = None

    completed_tasks: list[str] = field(default_factory=list)
    failed_tasks: list[str] = field(default_factory=list)

    shared_memory: Dict[str, Any] = field(default_factory=dict)

    iteration: int = 0

    started_at: datetime = field(default_factory=datetime.utcnow)

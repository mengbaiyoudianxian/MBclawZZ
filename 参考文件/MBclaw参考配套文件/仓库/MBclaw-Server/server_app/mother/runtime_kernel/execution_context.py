from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid


@dataclass
class ExecutionContext:
    task_id: str
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)

    memory: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

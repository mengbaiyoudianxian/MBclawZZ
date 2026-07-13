from dataclasses import dataclass, field
from typing import Dict, Any
import uuid
import time


@dataclass
class ExecutionContext:
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    permissions: Dict[str, Any] = field(default_factory=dict)
    limits: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

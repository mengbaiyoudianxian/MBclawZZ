from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid


@dataclass
class Event:

    type: str
    payload: Dict[str, Any]

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    source_module: str = "unknown"
    task_id: str = ""

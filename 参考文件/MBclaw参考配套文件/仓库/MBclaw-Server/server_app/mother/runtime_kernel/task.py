from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import uuid


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "generic"
    payload: Dict[str, Any] = field(default_factory=dict)

    priority: int = 5
    retry: int = 0
    max_retry: int = 3

    status: str = "PENDING"
    created_at: float = field(default_factory=time.time)

    trace_id: Optional[str] = None

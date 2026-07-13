from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time
import uuid


@dataclass(frozen=True)
class AuditEvent:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    actor: str  # user / worker / tool / scheduler

    action: str  # execute / plan / call_tool / retry / fail

    target: str  # tool / module / endpoint

    input: Dict[str, Any]

    output: Dict[str, Any]

    token_cost: float

    latency_ms: float

    success: bool

    timestamp: float = field(default_factory=lambda: time.time())

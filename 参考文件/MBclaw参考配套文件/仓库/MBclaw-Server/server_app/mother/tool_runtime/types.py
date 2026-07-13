from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import uuid


@dataclass
class ToolCall:
    tool_name: str
    args: Dict[str, Any]
    timeout: int = 30
    retry: int = 0


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    latency: float = 0.0
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

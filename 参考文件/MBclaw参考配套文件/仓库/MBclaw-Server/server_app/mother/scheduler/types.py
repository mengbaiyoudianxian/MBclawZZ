from dataclasses import dataclass
from typing import Dict, Any, Optional
import time
import uuid


@dataclass
class ModelRequest:
    task_type: str
    prompt: str
    max_tokens: int = 2048
    priority: int = 5
    budget: float = 1.0
    metadata: Dict[str, Any] = None
    trace_id: str = None


@dataclass
class ModelResponse:
    model: str
    output: str
    cost: float
    latency: float
    success: bool
    error: Optional[str] = None
    trace_id: str = None

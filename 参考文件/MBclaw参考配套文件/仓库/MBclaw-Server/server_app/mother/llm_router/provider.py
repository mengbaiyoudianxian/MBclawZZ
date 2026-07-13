from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class Provider:
    name: str
    model: str

    cost_per_1k_tokens: float
    avg_latency_ms: int
    success_rate: float

    handler: Callable[..., Any]

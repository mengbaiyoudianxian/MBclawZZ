from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class LLMRequest:
    task_type: str          # code / search / compress / chat
    prompt: str

    max_tokens: int = 1024
    temperature: float = 0.2

    priority: int = 1
    budget: float = 1.0     # max cost allowed

    context_length: int = 0


@dataclass
class LLMResponse:
    provider: str
    model: str
    output: str
    cost: float
    latency_ms: int

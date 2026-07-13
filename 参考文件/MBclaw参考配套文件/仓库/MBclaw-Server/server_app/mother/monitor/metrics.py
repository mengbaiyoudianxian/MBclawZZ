from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Dict


@dataclass
class MetricEvent:

    name: str
    value: float

    tags: Dict[str, str] = field(default_factory=dict)

    timestamp: float = field(default_factory=lambda: time.time())


class MetricRegistry:

    def __init__(self):

        self.buffer = []

    def emit(self, event: MetricEvent):

        self.buffer.append(event)

    def flush(self):

        data = self.buffer
        self.buffer = []
        return data

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class TraceEvent:
    event: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class TraceLogger:
    """
    Execution DAG + timeline recorder.
    """

    def __init__(self):
        self.events: List[TraceEvent] = []

    def log(self, event: str, payload: Dict[str, Any]):
        self.events.append(
            TraceEvent(event=event, payload=payload)
        )

    def export(self):
        return [
            {
                "event": e.event,
                "payload": e.payload,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in self.events
        ]

from __future__ import annotations

from typing import Any, Dict
import json
import time


class StructuredLogger:
    """
    JSON structured logging for execution tracing.
    """

    def log(self, event: str, payload: Dict[str, Any]):
        entry = {
            "event": event,
            "timestamp": time.time(),
            "payload": payload,
        }
        print(json.dumps(entry))

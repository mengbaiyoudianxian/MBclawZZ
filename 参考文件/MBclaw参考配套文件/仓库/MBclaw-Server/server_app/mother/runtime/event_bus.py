from __future__ import annotations

from typing import Any, Callable, Dict, List, DefaultDict
from collections import defaultdict


class EventBus:
    """
    Simple pub/sub event system for MBclaw runtime.
    """

    def __init__(self):
        self.subscribers: DefaultDict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable):
        self.subscribers[event].append(handler)

    def publish(self, event: str, payload: Dict[str, Any]):
        for handler in self.subscribers.get(event, []):
            try:
                handler(payload)
            except Exception:
                # isolate failures
                pass

from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime


class MemoryStore:
    """
    Minimal memory abstraction with governance hooks.
    """

    def __init__(self):
        self.store: Dict[str, Any] = {}

    def write(self, key: str, value: Any, context: Optional[Dict] = None):
        self.store[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {},
        }

    def read(self, key: str) -> Any:
        item = self.store.get(key)
        return item["value"] if item else None

    def delete(self, key: str):
        if key in self.store:
            del self.store[key]

    def dump(self):
        return self.store

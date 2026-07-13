from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import os

from .models import AuditRecord
from .enums import AuditLevel


class AuditLogger:
    """
    Persistent audit trail for all governed actions.
    """

    def __init__(self, path: str = "audit.log"):
        self.path = path
        self.buffer: List[AuditRecord] = []

    def log(
        self,
        level: AuditLevel,
        event: str,
        actor: Optional[str] = None,
        target: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        record = AuditRecord(
            level=level,
            event=event,
            actor=actor,
            target=target,
            data=data or {},
        )

        self.buffer.append(record)
        self._flush(record)

    def _flush(self, record: AuditRecord):
        line = record.model_dump_json()

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

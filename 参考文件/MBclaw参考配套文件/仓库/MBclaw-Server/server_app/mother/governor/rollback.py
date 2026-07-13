from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime

from .models import RollbackRecord
from .enums import RollbackReason


class RollbackManager:
    """
    Captures and restores system state snapshots.
    """

    def __init__(self):
        self.snapshots: List[RollbackRecord] = []

    def snapshot(
        self,
        state: Dict[str, Any],
        reason: RollbackReason,
        decision_id: Optional[str] = None,
    ) -> RollbackRecord:

        record = RollbackRecord(
            reason=reason,
            related_decision_id=decision_id,
            state_snapshot=state.copy(),
            success=False,
        )

        self.snapshots.append(record)
        return record

    def restore(self, record: RollbackRecord) -> Dict[str, Any]:
        """
        Restores a previous state snapshot.
        """
        record.success = True
        return record.state_snapshot

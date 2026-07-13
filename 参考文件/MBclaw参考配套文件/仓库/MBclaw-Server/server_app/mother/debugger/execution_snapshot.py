from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import copy


@dataclass
class ExecutionSnapshot:
    """
    Captures full runtime state for replay/debug.
    """

    state: Dict[str, Any] = field(default_factory=dict)
    plan: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)

    def clone(self) -> "ExecutionSnapshot":
        return ExecutionSnapshot(
            state=copy.deepcopy(self.state),
            plan=copy.deepcopy(self.plan),
            tasks=copy.deepcopy(self.tasks),
        )

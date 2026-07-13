from __future__ import annotations

from typing import Any, Dict

from .models import Action
from .enums import ActionType
from .exceptions import ExecutionBlocked


class Executor:
    """
    Executes approved actions only.
    """

    def run(self, action: Action) -> Any:
        if action.type == ActionType.TOOL_CALL:
            return self._run_tool(action)

        if action.type == ActionType.SYSTEM:
            return self._run_system(action)

        if action.type == ActionType.EXECUTE:
            return self._run_exec(action)

        raise ExecutionBlocked(f"Unsupported action type: {action.type}")

    def _run_tool(self, action: Action):
        # placeholder: integrate ToolRegistry later
        return {
            "tool": action.name,
            "status": "executed",
            "payload": action.payload,
        }

    def _run_system(self, action: Action):
        return {
            "system": action.name,
            "status": "executed",
        }

    def _run_exec(self, action: Action):
        return {
            "exec": action.name,
            "status": "executed",
        }

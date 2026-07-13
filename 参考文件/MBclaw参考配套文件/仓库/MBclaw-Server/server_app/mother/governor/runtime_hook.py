from __future__ import annotations

import functools
from typing import Any, Callable, Dict

from .models import Action
from .enums import ActionType


class RuntimeHook:
    """
    Intercepts tool execution or agent actions.
    Acts as a middleware layer.
    """

    def __init__(self, governor: "Governor"):
        self.governor = governor

    def wrap(self, func: Callable) -> Callable:
        """
        Decorator to intercept function execution.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            action = self._build_action(func, args, kwargs)

            # evaluate before execution
            proposal = self._to_proposal(action)

            decision = self.governor.evaluate(proposal)

            if decision.status.value != "approved":
                raise PermissionError(
                    f"Blocked by Governor: {decision.reason}"
                )

            return func(*args, **kwargs)

        return wrapper

    def _build_action(self, func: Callable, args, kwargs) -> Action:
        return Action(
            type=ActionType.TOOL_CALL,
            name=func.__name__,
            payload={
                "args": str(args),
                "kwargs": str(kwargs),
            },
        )

    def _to_proposal(self, action: Action):
        from .models import Proposal, ContextState

        return Proposal(
            actions=[action],
            context=ContextState(),
            rationale=f"runtime_hook:{action.name}",
        )

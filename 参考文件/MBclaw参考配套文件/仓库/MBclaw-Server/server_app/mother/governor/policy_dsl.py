from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Callable


@dataclass
class PolicyRule:
    name: str
    expr: Callable[[Dict[str, Any]], bool]
    action: str  # allow | deny | review


class PolicyDSL:
    """
    Simple executable policy language.
    """

    def __init__(self):
        self.rules: list[PolicyRule] = []

    def rule(self, name: str, expr: Callable, action: str):
        self.rules.append(
            PolicyRule(name=name, expr=expr, action=action)
        )

    def evaluate(self, context: Dict[str, Any]) -> str:
        for r in self.rules:
            if r.expr(context):
                return r.action

        return "allow"

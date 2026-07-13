from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional

from .enums import ActionType, RiskLevel


@dataclass
class Rule:
    rule_id: str
    name: str
    description: str

    # predicate: return True if rule applies
    predicate: Callable[[Dict[str, Any]], bool]

    # evaluator: returns score or decision modifier
    evaluator: Callable[[Dict[str, Any]], Dict[str, Any]]

    priority: int = 0
    enabled: bool = True


@dataclass
class Constitution:
    """
    Core rule registry.
    Governor policy is driven by a set of executable rules.
    """

    rules: List[Rule] = field(default_factory=list)

    def register(self, rule: Rule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def evaluate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []

        for rule in self.rules:
            if not rule.enabled:
                continue

            try:
                if rule.predicate(context):
                    result = rule.evaluator(context)
                    result["rule_id"] = rule.rule_id
                    result["rule_name"] = rule.name
                    results.append(result)
            except Exception as e:
                results.append({
                    "rule_id": rule.rule_id,
                    "error": str(e),
                    "severity": "rule_execution_error"
                })

        return results


# -------------------------
# Default rule templates
# -------------------------

def always_allow(_: Dict[str, Any]) -> bool:
    return True


def always_deny(_: Dict[str, Any]) -> bool:
    return True


def risk_threshold_rule(threshold: RiskLevel):
    def predicate(ctx: Dict[str, Any]) -> bool:
        return ctx.get("risk", 0) >= threshold

    def evaluator(ctx: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "action": "block",
            "reason": f"risk >= {threshold}"
        }

    return Rule(
        rule_id=f"risk_block_{threshold}",
        name="Risk Threshold Rule",
        description="Blocks actions above risk threshold",
        predicate=predicate,
        evaluator=evaluator,
        priority=100
    )

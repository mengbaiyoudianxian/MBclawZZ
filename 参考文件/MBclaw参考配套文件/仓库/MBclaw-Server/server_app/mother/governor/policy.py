from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .enums import DecisionStatus, RiskLevel
from .exceptions import PolicyViolation


@dataclass
class PolicyResult:
    allowed: bool
    status: DecisionStatus
    reasons: List[str]
    metadata: Dict[str, Any]


class PolicyEngine:
    """
    Evaluates whether a proposal is allowed under governance rules.
    """

    def __init__(self):
        self.max_risk = RiskLevel.HIGH

        self.blocked_actions = {
            "self_modify_kernel",
            "delete_system_root",
        }

    def evaluate(self, proposal: Dict[str, Any], risk_level: RiskLevel) -> PolicyResult:

        reasons = []

        # 1. risk gate
        if risk_level > self.max_risk:
            raise PolicyViolation(
                "Risk exceeds policy threshold",
                policy_id="risk_gate"
            )

        # 2. action blacklist
        for action in proposal.get("actions", []):
            if action.get("name") in self.blocked_actions:
                raise PolicyViolation(
                    f"Blocked action: {action.get('name')}",
                    policy_id="action_blacklist"
                )

        # 3. contextual constraints
        context = proposal.get("context", {})
        if context.get("environment") == "production":
            for action in proposal.get("actions", []):
                if action.get("type") == "DELETE":
                    reasons.append("delete_in_production_restricted")

        allowed = len(reasons) == 0

        status = DecisionStatus.APPROVED if allowed else DecisionStatus.REJECTED

        return PolicyResult(
            allowed=allowed,
            status=status,
            reasons=reasons,
            metadata={
                "risk_level": risk_level,
                "policy": "v1_core"
            }
        )

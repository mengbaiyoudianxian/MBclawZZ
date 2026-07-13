from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .models import Proposal, Decision
from .enums import DecisionStatus


@dataclass
class ApprovalStep:
    step_id: str
    name: str
    required: bool = True


class ApprovalPipeline:
    """
    Optional multi-stage approval system.
    """

    def __init__(self):
        self.steps: List[ApprovalStep] = [
            ApprovalStep("risk", "Risk Check"),
            ApprovalStep("policy", "Policy Check"),
            ApprovalStep("audit", "Audit Log"),
        ]

    def run(self, proposal: Proposal, decision: Decision) -> Decision:
        """
        Could be extended into human-in-the-loop / multi-agent review.
        """

        if decision.status != DecisionStatus.APPROVED:
            return decision

        # placeholder for future human review stages
        for step in self.steps:
            if step.required and decision.final_risk.value >= 3:
                decision.status = DecisionStatus.REVIEW
                decision.reason = f"Requires review at step: {step.name}"
                break

        return decision

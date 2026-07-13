from __future__ import annotations

from typing import Any, Dict, List, Optional

from .models import Proposal, Decision, Action, ContextState
from .enums import DecisionStatus, RiskLevel
from .risk import RiskEngine
from .policy import PolicyEngine, PolicyResult
from .exceptions import ExecutionBlocked


class Governor:
    """
    Core orchestration layer:
    Proposal -> Risk -> Policy -> Decision
    """

    def __init__(
        self,
        risk_engine: Optional[RiskEngine] = None,
        policy_engine: Optional[PolicyEngine] = None,
    ):
        self.risk_engine = risk_engine or RiskEngine()
        self.policy_engine = policy_engine or PolicyEngine()

    # -------------------------
    # Public API
    # -------------------------

    def evaluate(self, proposal: Proposal) -> Decision:
        """
        Main evaluation pipeline.
        """

        risk = self.risk_engine.score_proposal(proposal.model_dump())
        risk_level = risk.level

        policy_result: PolicyResult = self.policy_engine.evaluate(
            proposal.model_dump(),
            risk_level,
        )

        decision = Decision(
            proposal_id=proposal.proposal_id,
            status=policy_result.status,
            final_risk=risk_level,
            reason=";".join(policy_result.reasons) if policy_result.reasons else None,
            policy_trace=[str(policy_result.metadata)],
            risk_trace=[str(risk.breakdown)],
            approved_actions=[],
        )

        if not policy_result.allowed:
            decision.status = DecisionStatus.REJECTED

        return decision

    def execute(self, proposal: Proposal, executor: "Executor") -> Decision:
        """
        Evaluate + optionally execute approved actions.
        """

        decision = self.evaluate(proposal)

        if decision.status != DecisionStatus.APPROVED:
            raise ExecutionBlocked(
                "Proposal rejected by Governor",
                action_id=proposal.proposal_id,
            )

        approved = []

        for action in proposal.actions:
            executor.run(action)
            approved.append(action.action_id)

        decision.approved_actions = approved
        return decision

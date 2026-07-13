from __future__ import annotations

from typing import Any, Dict

from .governor import Governor
from .models import Proposal, Action, ContextState
from .executor import Executor
from .audit import AuditLogger
from .tools import ToolRegistry
from .enums import AuditLevel


class Agent:
    """
    High-level controlled agent runtime.
    Everything flows through Governor.
    """

    def __init__(self):
        self.governor = Governor()
        self.executor = Executor()
        self.audit = AuditLogger()
        self.tools = ToolRegistry()

    def act(self, actions: list[Action], context: ContextState) -> Any:

        proposal = Proposal(
            actions=actions,
            context=context,
            rationale="agent_act",
        )

        self.audit.log(
            AuditLevel.INFO,
            "proposal_created",
            data={"proposal_id": proposal.proposal_id},
        )

        decision = self.governor.evaluate(proposal)

        self.audit.log(
            AuditLevel.INFO,
            "decision_made",
            data={
                "proposal_id": proposal.proposal_id,
                "status": decision.status,
                "risk": str(decision.final_risk),
            },
        )

        if decision.status.value != "approved":
            self.audit.log(
                AuditLevel.WARN,
                "execution_blocked",
                data={"reason": decision.reason},
            )
            return None

        results = []
        for action in actions:
            result = self.executor.run(action)
            results.append(result)

        self.audit.log(
            AuditLevel.INFO,
            "execution_completed",
            data={"count": len(results)},
        )

        return results

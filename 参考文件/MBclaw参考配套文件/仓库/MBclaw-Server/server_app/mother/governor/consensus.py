from __future__ import annotations

from typing import List, Dict, Any

from .governor import Governor
from .models import Proposal, Decision


class ConsensusGovernor:
    """
    Runs multiple governance policies and aggregates decision.
    """

    def __init__(self, governors: List[Governor]):
        self.governors = governors

    def evaluate(self, proposal: Proposal) -> Dict[str, Any]:
        results: List[Decision] = []

        for g in self.governors:
            try:
                results.append(g.evaluate(proposal))
            except Exception as e:
                results.append(
                    Decision(
                        proposal_id=proposal.proposal_id,
                        status="rejected",
                        final_risk=4,
                        reason=str(e),
                    )
                )

        approved = sum(1 for r in results if r.status.value == "approved")

        consensus = approved > len(results) // 2

        return {
            "consensus": consensus,
            "votes": [r.model_dump() for r in results],
        }

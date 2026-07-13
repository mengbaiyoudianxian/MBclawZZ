from __future__ import annotations


class GovernorBridge:

    def request_approval(self, prt: dict):

        # low risk auto-approve, high risk manual review
        if prt["type"] == "workflow_restructure":
            return "manual_review_required"

        return "auto_approved"

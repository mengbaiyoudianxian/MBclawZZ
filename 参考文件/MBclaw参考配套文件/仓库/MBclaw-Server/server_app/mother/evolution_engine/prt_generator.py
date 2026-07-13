from __future__ import annotations

import uuid


class PRTGenerator:

    def generate(self, analysis: dict, patterns: dict):

        proposals = []

        # slow task optimization
        for slow in analysis["slow"]:

            proposals.append({
                "id": str(uuid.uuid4()),
                "type": "scheduler_adjustment",
                "action": "switch_to_fast_model",
                "target": slow["target"],
                "reason": "high_latency_detected"
            })

        # high cost optimization
        for expensive in analysis["expensive"]:

            proposals.append({
                "id": str(uuid.uuid4()),
                "type": "token_optimization",
                "action": "enable_context_compression",
                "target": expensive["target"],
                "reason": "high_token_cost"
            })

        # repeated failure optimization
        for p in patterns.get("repeated_failures", []):

            proposals.append({
                "id": str(uuid.uuid4()),
                "type": "workflow_restructure",
                "action": "add_fallback_path",
                "target": p["target"],
                "reason": "repeated_failure"
            })

        return proposals

from __future__ import annotations

from typing import List
import uuid

from engineering_brain.registry import EngineeringRegistry
from engineering_brain.knowledge import EngineeringKnowledge
from engineering_brain.tech_debt import TechDebt


class EvolutionBridge:

    def __init__(self, registry: EngineeringRegistry):

        self.registry = registry

    # -------------------------
    # extract experience from runtime results
    # -------------------------

    def absorb(self, evolution_signals: List[dict]):

        for s in evolution_signals:

            # bug -> knowledge
            if s.get("type") == "bug":

                self.registry.add_knowledge(
                    EngineeringKnowledge(
                        id=str(uuid.uuid4()),
                        type="bug",
                        title=s["title"],
                        content=s["content"],
                        confidence=s.get("confidence", 0.6),
                        tags=s.get("tags", [])
                    )
                )

            # system failure -> tech debt
            if s.get("type") == "debt":

                self.registry.add_debt(
                    TechDebt(
                        id=str(uuid.uuid4()),
                        module=s["module"],
                        description=s["description"],
                        severity=s.get("severity", 0.5),
                        impact_area=s.get("impact", []),
                        suggested_fix=s.get("fix", "")
                    )
                )

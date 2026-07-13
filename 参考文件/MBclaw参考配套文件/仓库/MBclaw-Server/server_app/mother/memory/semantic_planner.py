from __future__ import annotations

from typing import List, Dict, Any

from planner.models import Plan, Task
from .vector_store import VectorStore


class SemanticPlanner:
    """
    Enhances planning using semantic memory retrieval.
    """

    def __init__(self, memory: VectorStore):
        self.memory = memory

    def enrich_plan(self, plan: Plan, query_vec: List[float]) -> Plan:

        similar = self.memory.search(query_vec)

        if not similar:
            return plan

        # inject memory-driven tasks
        for _, key in similar:
            plan.tasks.append(
                Task(
                    name=f"memory_hint_{key}",
                    description="Retrieved from semantic memory",
                    required_capabilities=["reasoning"],
                    estimated_cost=1,
                )
            )

        plan.version += 1
        plan.status = "memory_enriched"

        return plan

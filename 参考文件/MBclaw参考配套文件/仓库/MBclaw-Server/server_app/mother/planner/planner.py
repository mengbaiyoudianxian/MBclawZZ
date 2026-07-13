from __future__ import annotations

from typing import Dict, List

from .models import Plan
from .decomposer import TaskDecomposer
from .dependency import DependencyResolver
from .replanner import RePlanner


class Planner:
    """
    Main orchestration layer:
    goal → plan → task graph → execution order
    """

    def __init__(self):
        self.decomposer = TaskDecomposer()
        self.resolver = DependencyResolver()
        self.replanner = RePlanner()

    def create_plan(self, goal: str, context: dict) -> Plan:
        plan = self.decomposer.decompose(goal, context)
        return plan

    def execution_order(self, plan: Plan) -> List[str]:
        return self.resolver.resolve(plan)

    def handle_failure(self, plan: Plan, task_id: str, reason: str) -> Plan:
        return self.replanner.replan(plan, task_id, reason)

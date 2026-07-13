from __future__ import annotations

from typing import List

from .models import Task, Plan


class TaskDecomposer:
    """
    Converts high-level goal → structured task graph
    """

    def decompose(self, goal: str, context: dict) -> Plan:

        tasks = []

        # heuristic decomposition (v1 simple but deterministic)
        if "bug" in goal.lower():
            tasks = [
                Task(
                    name="reproduce_bug",
                    description="Reproduce the issue reliably",
                    required_capabilities=["debugging", "logging"],
                    estimated_cost=2,
                ),
                Task(
                    name="analyze_root_cause",
                    description="Find root cause of bug",
                    dependencies=[],
                    required_capabilities=["debugging", "code_analysis"],
                    estimated_cost=4,
                ),
                Task(
                    name="apply_fix",
                    description="Implement fix",
                    required_capabilities=["code_edit"],
                    dependencies=[],
                    estimated_cost=3,
                ),
                Task(
                    name="validate_fix",
                    description="Run tests and validate",
                    required_capabilities=["testing"],
                    dependencies=[],
                    estimated_cost=2,
                ),
            ]

        elif "build" in goal.lower():
            tasks = [
                Task(
                    name="design_architecture",
                    description="Design system architecture",
                    required_capabilities=["system_design"],
                    estimated_cost=5,
                ),
                Task(
                    name="implement_core",
                    description="Implement core modules",
                    required_capabilities=["code_edit"],
                    estimated_cost=6,
                ),
                Task(
                    name="integration",
                    description="Integrate components",
                    required_capabilities=["integration"],
                    estimated_cost=4,
                ),
            ]

        else:
            tasks = [
                Task(
                    name="analyze_goal",
                    description="Understand objective",
                    required_capabilities=["reasoning"],
                    estimated_cost=1,
                )
            ]

        return Plan(
            goal=goal,
            tasks=tasks,
            context=context,
        )

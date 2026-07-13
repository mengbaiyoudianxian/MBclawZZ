from __future__ import annotations

from typing import Dict

from planner.models import Task


class SchedulingPolicy:
    """
    Determines execution ordering adjustments.
    """

    def score_task(self, task: Task) -> float:
        score = task.estimated_cost

        if "critical" in task.name:
            score += 5

        if task.required_capabilities:
            score += len(task.required_capabilities) * 0.5

        return score

    def adjust_priority(self, task: Task) -> int:
        base = task.priority

        if task.estimated_cost > 5:
            base += 2

        if "validate" in task.name:
            base += 3

        return base

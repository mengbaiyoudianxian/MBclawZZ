from __future__ import annotations

from planner.models import Task


class CapabilityConstraints:
    """
    Applies execution constraints before scheduling.
    """

    def validate(self, task: Task) -> bool:
        # basic safety constraint
        if "root" in task.name:
            return False

        if task.estimated_cost > 10 and "optimization" not in task.required_capabilities:
            return False

        return True

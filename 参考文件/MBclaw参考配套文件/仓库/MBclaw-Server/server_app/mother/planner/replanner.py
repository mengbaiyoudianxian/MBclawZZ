from __future__ import annotations

from typing import List, Dict

from .models import Plan, Task


class RePlanner:
    """
    Dynamically modifies plan during execution failure or new signals.
    """

    def replan(self, plan: Plan, failed_task_id: str, reason: str) -> Plan:

        new_tasks: List[Task] = []

        for task in plan.tasks:
            if task.task_id == failed_task_id:
                # inject recovery task
                new_tasks.append(
                    Task(
                        name="recover_" + task.name,
                        description=f"Recovery for {task.name}: {reason}",
                        required_capabilities=task.required_capabilities,
                        estimated_cost=task.estimated_cost + 1,
                        dependencies=task.dependencies,
                    )
                )
            else:
                new_tasks.append(task)

        plan.tasks = new_tasks
        plan.version += 1
        plan.status = "replanned"

        return plan

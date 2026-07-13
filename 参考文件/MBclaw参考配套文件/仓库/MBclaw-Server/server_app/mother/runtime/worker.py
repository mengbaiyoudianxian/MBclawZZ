from __future__ import annotations

from typing import Any, Dict

from planner.models import Task
from capability.registry import ExtendedCapabilityRegistry


class Worker:
    """
    Executes a single task using capability handlers.
    """

    def __init__(self, registry: ExtendedCapabilityRegistry):
        self.registry = registry

    def execute(self, task: Task) -> Dict[str, Any]:
        results = {}

        for cap in task.required_capabilities:
            # each capability is executed independently
            result = self.registry.execute(
                cap,
                task=task.name,
                inputs=task.inputs,
            )
            results[cap] = result

        task.status = "done"
        task.outputs = results

        return results

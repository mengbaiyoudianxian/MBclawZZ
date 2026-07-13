from __future__ import annotations

from typing import List

from planner.models import Task
from .registry import CapabilityRegistry


class CapabilityMatcher:
    """
    Matches tasks to available capabilities.
    """

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def match(self, task: Task) -> bool:
        for cap in task.required_capabilities:
            if not self.registry.has(cap):
                return False
        return True

    def missing(self, task: Task) -> List[str]:
        return [
            c for c in task.required_capabilities
            if not self.registry.has(c)
        ]

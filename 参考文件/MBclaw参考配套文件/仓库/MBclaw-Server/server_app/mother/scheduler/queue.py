from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import heapq

from planner.models import Task


@dataclass(order=True)
class PrioritizedTask:
    priority: int
    task: Task = field(compare=False)


class TaskQueue:
    """
    Priority-based task queue (min-heap inverted for max-priority)
    """

    def __init__(self):
        self._heap: List[PrioritizedTask] = []

    def push(self, task: Task):
        heapq.heappush(
            self._heap,
            PrioritizedTask(priority=-task.priority, task=task)
        )

    def pop(self) -> Optional[Task]:
        if not self._heap:
            return None
        return heapq.heappop(self._heap).task

    def empty(self) -> bool:
        return len(self._heap) == 0

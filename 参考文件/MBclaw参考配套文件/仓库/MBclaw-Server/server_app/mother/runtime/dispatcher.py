from __future__ import annotations

from typing import Optional

from scheduler.scheduler import Scheduler
from planner.models import Task


class Dispatcher:
    """
    Pulls tasks from scheduler and assigns them to workers.
    """

    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def get_next_task(self) -> Optional[Task]:
        return self.scheduler.next_task()

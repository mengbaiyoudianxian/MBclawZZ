from __future__ import annotations

import asyncio
from typing import Any, List

from planner.models import Task
from runtime.worker import Worker


class AsyncWorkerPool:
    """
    Concurrent execution layer for tasks.
    """

    def __init__(self, worker: Worker, concurrency: int = 4):
        self.worker = worker
        self.semaphore = asyncio.Semaphore(concurrency)

    async def run_task(self, task: Task):
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                self.worker.execute,
                task,
            )

    async def run_batch(self, tasks: List[Task]):
        return await asyncio.gather(
            *[self.run_task(t) for t in tasks]
        )

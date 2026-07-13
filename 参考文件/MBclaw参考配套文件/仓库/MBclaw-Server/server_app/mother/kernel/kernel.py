import asyncio
from collections import deque

from runtime_kernel.task import Task
from runtime_kernel.execution_context import ExecutionContext
from execution.executor import Executor


class Kernel:
    def __init__(self, eventbus, planner, scheduler, memory):
        self.eventbus = eventbus
        self.planner = planner
        self.scheduler = scheduler
        self.memory = memory

        self.task_queue = deque()
        self.executor = Executor()

        self.running = False

    def submit(self, task: Task):
        self.task_queue.append(task)

    async def run(self):
        self.running = True

        while self.running:
            if not self.task_queue:
                await asyncio.sleep(0.1)
                continue

            task = self.task_queue.popleft()
            context = ExecutionContext(task_id=task.id)

            try:
                await self.eventbus.publish("task.started", {"task_id": task.id})

                plan = await self.planner.generate(task)

                model = await self.scheduler.select(plan)

                result = await self.executor.run(task, context)

                await self.memory.write(task, result)

                await self.eventbus.publish("task.completed", result)

            except Exception as e:
                task.status = "FAILED"

                await self.memory.write(task, {"error": str(e)})

                await self.eventbus.publish("task.failed", {
                    "task_id": task.id,
                    "error": str(e)
                })

                if task.retry < task.max_retry:
                    task.retry += 1
                    self.task_queue.append(task)

    def stop(self):
        self.running = False

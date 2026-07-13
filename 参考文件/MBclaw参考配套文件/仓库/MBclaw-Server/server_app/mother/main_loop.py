import asyncio

from kernel.kernel import Kernel
from eventbus.bus import EventBus
from runtime_kernel.task import Task


class DummyPlanner:
    async def generate(self, task):
        return {"steps": ["exec"], "task_id": task.id}


class DummyScheduler:
    async def select(self, plan):
        return {"model": "default"}


class DummyMemory:
    async def write(self, task, result):
        print("[MEMORY]", task.id, result)


async def main():
    bus = EventBus()

    kernel = Kernel(
        eventbus=bus,
        planner=DummyPlanner(),
        scheduler=DummyScheduler(),
        memory=DummyMemory()
    )

    bus.subscribe("task.started", lambda p: print("EVENT started", p))
    bus.subscribe("task.completed", lambda p: print("EVENT completed", p))
    bus.subscribe("task.failed", lambda p: print("EVENT failed", p))

    asyncio.create_task(bus._dispatch_loop())

    asyncio.create_task(kernel.run())

    for i in range(3):
        kernel.submit(Task(payload={"i": i}))

    await asyncio.sleep(3)
    kernel.stop()


if __name__ == "__main__":
    asyncio.run(main())

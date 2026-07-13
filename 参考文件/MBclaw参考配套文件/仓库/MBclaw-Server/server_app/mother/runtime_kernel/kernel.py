from queue import PriorityQueue

from runtime_kernel.task import Task
from runtime_kernel.worker_pool import WorkerPool
from runtime_kernel.event_bus import EventBus
from runtime_kernel.execution_context import ExecutionContext
from runtime_kernel.result_collector import ResultCollector
from runtime_kernel.memory_adapter import MemoryAdapter


class RuntimeKernel:

    def __init__(self):

        self.queue = PriorityQueue()

        self.event_bus = EventBus()

        self.memory = MemoryAdapter()

        self.worker_pool = WorkerPool(size=3)

        self.collector = ResultCollector(self.memory, self.event_bus)

    def submit_task(self, task: Task):

        self.queue.put((task.priority, task))

        self.event_bus.emit("task_created", task.__dict__)

    def step(self):

        if self.queue.empty():
            return

        _, task = self.queue.get()

        worker = self.worker_pool.acquire()

        context = ExecutionContext(
            task_id=task.id,
            worker_id=worker.id
        )

        result = worker.run(task, context)

        self.collector.collect(result)

        self.event_bus.emit("task_finished", result)

    def run_loop(self, steps=10):

        for _ in range(steps):
            self.step()

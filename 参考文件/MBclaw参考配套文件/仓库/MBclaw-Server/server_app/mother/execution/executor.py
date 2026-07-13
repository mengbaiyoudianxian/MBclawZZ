from runtime_kernel.worker import Worker


class Executor:
    def __init__(self):
        self.worker = Worker("worker-1")

    async def run(self, task, context):
        return await self.worker.run(task, context)

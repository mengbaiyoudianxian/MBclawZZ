import asyncio


class Worker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.state = "IDLE"

    async def run(self, task, context):
        self.state = "RUNNING"

        await asyncio.sleep(0.2)

        result = {
            "task_id": task.id,
            "worker_id": self.worker_id,
            "output": f"processed:{task.payload}",
            "success": True,
        }

        self.state = "IDLE"
        return result

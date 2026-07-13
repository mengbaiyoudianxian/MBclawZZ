import asyncio
from collections import defaultdict


class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queue = asyncio.Queue()

    def subscribe(self, event_type: str, callback):
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, payload: dict):
        await self.queue.put((event_type, payload))

    async def _dispatch_loop(self):
        while True:
            event_type, payload = await self.queue.get()

            for cb in self.subscribers.get(event_type, []):
                asyncio.create_task(cb(payload))

            # wildcard
            for key, cbs in self.subscribers.items():
                if key.endswith("*"):
                    prefix = key[:-1]
                    if event_type.startswith(prefix):
                        for cb in cbs:
                            asyncio.create_task(cb(payload))

    def start(self):
        return asyncio.create_task(self._dispatch_loop())

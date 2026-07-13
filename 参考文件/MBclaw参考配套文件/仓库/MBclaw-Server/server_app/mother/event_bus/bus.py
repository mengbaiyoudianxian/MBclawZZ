import asyncio

from event_bus.router import EventRouter
from event_bus.types import Event


class EventBus:

    def __init__(self):

        self.router = EventRouter()

        self.queue = asyncio.Queue()

        self.running = False

    # subscribe / unsubscribe

    def subscribe(self, event_type: str, callback):

        self.router.add(event_type, callback)

    def unsubscribe(self, event_type: str, callback):

        self.router.remove(event_type, callback)

    # publish

    async def publish(self, event: Event):

        await self.queue.put(event)

    # dispatch loop

    async def _dispatch_loop(self):

        while self.running:

            event = await self.queue.get()

            callbacks = self.router.match(event.type)

            for cb in callbacks:

                try:

                    if asyncio.iscoroutinefunction(cb):
                        await cb(event)
                    else:
                        cb(event)

                except Exception as e:
                    print(f"[EventBus Error] {event.type}: {e}")

    # lifecycle

    async def start(self):

        self.running = True

        asyncio.create_task(self._dispatch_loop())

    async def stop(self):

        self.running = False

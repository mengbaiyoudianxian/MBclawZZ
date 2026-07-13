class EventBus:

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, fn):

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(fn)

    def emit(self, event_type: str, data):

        for fn in self.subscribers.get(event_type, []):
            try:
                fn(data)
            except Exception as e:
                print(f"[EventBus Error] {event_type}: {e}")

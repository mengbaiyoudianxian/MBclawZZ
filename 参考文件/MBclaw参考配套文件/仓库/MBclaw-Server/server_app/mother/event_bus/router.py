import fnmatch


class EventRouter:

    def __init__(self):
        self.routes = {}

    def add(self, event_type: str, callback):

        if event_type not in self.routes:
            self.routes[event_type] = []

        self.routes[event_type].append(callback)

    def remove(self, event_type: str, callback):

        if event_type in self.routes:
            self.routes[event_type].remove(callback)

    def match(self, event_type: str):

        matched = []

        for pattern, callbacks in self.routes.items():

            if fnmatch.fnmatch(event_type, pattern):
                matched.extend(callbacks)

        return matched

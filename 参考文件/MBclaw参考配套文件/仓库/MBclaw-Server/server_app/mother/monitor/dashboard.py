from __future__ import annotations


class DashboardState:

    def __init__(self):

        self.state = {
            "cpu": [],
            "ram": [],
            "latency": [],
            "tokens": []
        }

    def update(self, events):

        for e in events:

            if e.name in self.state:

                self.state[e.name].append(e.value)

    def snapshot(self):

        return self.state

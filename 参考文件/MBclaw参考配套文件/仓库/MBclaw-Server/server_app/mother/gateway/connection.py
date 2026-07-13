from __future__ import annotations

import time


class ConnectionManager:

    def __init__(self):
        self.connections = {}

    # register connection
    def connect(self, source: str, conn):

        self.connections[source] = {
            "conn": conn,
            "last_heartbeat": time.time(),
            "status": "alive"
        }

    # heartbeat update
    def heartbeat(self, source: str):

        if source in self.connections:
            self.connections[source]["last_heartbeat"] = time.time()

    # detect disconnection
    def check_health(self, timeout=30):

        now = time.time()

        for k, v in self.connections.items():

            if now - v["last_heartbeat"] > timeout:
                v["status"] = "dead"

    # auto reconnect
    def reconnect(self, source: str, conn_factory):

        self.connections[source] = {
            "conn": conn_factory(),
            "last_heartbeat": time.time(),
            "status": "alive"
        }

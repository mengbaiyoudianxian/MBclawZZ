from __future__ import annotations

from audit.log_store import AppendOnlyAuditLog


class AuditReplayEngine:

    def __init__(self, store: AppendOnlyAuditLog):

        self.store = store

    # -----------------------------
    # full system behavior replay
    # -----------------------------

    def replay(self):

        events = self.store.load()

        state = {}

        for e in events:

            state[e.id] = {
                "actor": e.actor,
                "action": e.action,
                "target": e.target,
                "input": e.input,
                "output": e.output,
                "success": e.success
            }

        return state

from __future__ import annotations

from audit.event import AuditEvent
from audit.log_store import AppendOnlyAuditLog


class AuditRecorder:

    def __init__(self, store: AppendOnlyAuditLog):

        self.store = store

    # -----------------------------
    # record a complete call chain
    # -----------------------------

    def record(self,
               actor: str,
               action: str,
               target: str,
               input: dict,
               output: dict,
               token_cost: float,
               latency_ms: float,
               success: bool):

        event = AuditEvent(
            actor=actor,
            action=action,
            target=target,
            input=input,
            output=output,
            token_cost=token_cost,
            latency_ms=latency_ms,
            success=success
        )

        self.store.append(event)

        return event

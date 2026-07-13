from __future__ import annotations

import json
from typing import List
from audit.event import AuditEvent


class AppendOnlyAuditLog:

    def __init__(self, file_path="audit.log"):

        self.file_path = file_path

    # -----------------------------
    # write (immutable, append-only)
    # -----------------------------

    def append(self, event: AuditEvent):

        with open(self.file_path, "a") as f:

            f.write(json.dumps(event.__dict__) + "\n")

    # -----------------------------
    # read (for replay)
    # -----------------------------

    def load(self) -> List[AuditEvent]:

        events = []

        try:
            with open(self.file_path, "r") as f:

                for line in f:

                    data = json.loads(line.strip())

                    events.append(AuditEvent(**data))

        except FileNotFoundError:
            pass

        return events

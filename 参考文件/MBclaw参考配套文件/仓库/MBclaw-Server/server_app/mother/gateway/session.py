from __future__ import annotations

from typing import Dict, List
from gateway.message import UnifiedMessage


class SessionManager:

    def __init__(self):
        self.sessions: Dict[str, List[UnifiedMessage]] = {}

    def append(self, msg: UnifiedMessage):

        sid = msg.session_id

        if sid not in self.sessions:
            self.sessions[sid] = []

        self.sessions[sid].append(msg)

    def get(self, session_id: str):
        return self.sessions.get(session_id, [])

from __future__ import annotations

import sqlite3
import json
from typing import Any, Dict, Optional


class StateStore:
    """
    Minimal persistence layer (SQLite-backed).
    """

    def __init__(self, db_path: str = "mbclaw.db"):
        self.conn = sqlite3.connect(db_path)
        self._init()

    def _init(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS runtime_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        self.conn.commit()

    def set(self, key: str, value: Dict[str, Any]):
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO runtime_state (key, value) VALUES (?, ?)",
            (key, json.dumps(value)),
        )
        self.conn.commit()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM runtime_state WHERE key=?", (key,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

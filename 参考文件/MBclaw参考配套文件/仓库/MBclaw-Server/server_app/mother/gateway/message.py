from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class UnifiedMessage:

    # source platform
    source: str  # qq / wechat / feishu / web / cli / api

    # user ID (cross-platform mapped)
    user_id: str

    # session ID
    session_id: str

    # message type
    type: str  # text / image / command / event

    # content
    content: str

    # metadata (device/platform/permission)
    meta: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=lambda: time.time())

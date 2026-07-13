from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import time


@dataclass
class MutationSpec:

    id: str

    type: str
    # policy / routing / scheduler / memory / tool_weight

    target: str

    patch: Dict[str, Any]

    reason: str

    confidence: float

    created_at: float = time.time()

    status: str = "proposed"  # approved / rejected / applied

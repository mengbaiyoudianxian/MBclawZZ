from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import time


@dataclass
class TechDebt:

    id: str

    module: str

    description: str

    severity: float  # 0-1

    impact_area: list

    suggested_fix: str

    meta: Dict[str, Any] = None

    created_at: float = time.time()

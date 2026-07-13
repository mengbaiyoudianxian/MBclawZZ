from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class EvolutionSignal:

    type: str  # success / failure / repetition / conflict / efficiency

    weight: float

    source: str  # memory / runtime / skill / tool

    context: Dict

    tags: List[str] = field(default_factory=list)

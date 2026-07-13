from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class SystemIR:

    modules: Dict[str, Any]

    dependencies: Dict[str, List[str]]

    policies: Dict[str, Any]

    execution_flows: List[Dict]

    version: str = "v1"

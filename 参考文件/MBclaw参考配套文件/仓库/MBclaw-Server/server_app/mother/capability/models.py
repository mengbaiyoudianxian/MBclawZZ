from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class CapabilityIO:
    name: str
    type: str  # string / json / binary / dict


@dataclass
class CapabilityVersion:
    version: str
    dependencies: List[str] = field(default_factory=list)
    deprecated: bool = False


@dataclass
class Capability:
    """
    Standardized capability definition (Tool / Skill / Plugin / Workflow unified)
    """

    name: str
    type: str  # tool / skill / workflow / plugin

    description: str

    inputs: List[CapabilityIO]
    outputs: List[CapabilityIO]

    permission: str  # low / medium / high / system

    mcp_mapping: Optional[str] = None  # MCP bridge id

    version: CapabilityVersion = field(default_factory=lambda: CapabilityVersion("1.0.0"))

    metadata: Dict[str, Any] = field(default_factory=dict)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List
import json
import hashlib


@dataclass
class PackageSpec:
    name: str
    version: str

    type: str  # MCP / skill / plugin / workflow / prompt

    entry: str

    dependencies: List[str] = field(default_factory=list)

    permissions: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    signature: str = ""

    def serialize(self) -> str:
        payload = {
            "name": self.name,
            "version": self.version,
            "type": self.type,
            "entry": self.entry,
            "dependencies": self.dependencies,
            "permissions": self.permissions,
            "metadata": self.metadata,
        }
        return json.dumps(payload, sort_keys=True)

    def sign(self, secret: str):
        self.signature = hashlib.sha256((self.serialize() + secret).encode()).hexdigest()

    def verify(self, secret: str) -> bool:
        return hashlib.sha256((self.serialize() + secret).encode()).hexdigest() == self.signature

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List
import json
import hashlib


@dataclass
class CapPackage:
    """
    .cap capability package format
    """

    name: str
    version: str

    entry: str  # entry function path
    description: str

    dependencies: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    signature: str = ""

    def serialize(self) -> str:
        payload = {
            "name": self.name,
            "version": self.version,
            "entry": self.entry,
            "description": self.description,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
        }
        return json.dumps(payload, sort_keys=True)

    def sign(self, secret: str):
        raw = self.serialize() + secret
        self.signature = hashlib.sha256(raw.encode()).hexdigest()

    def verify(self, secret: str) -> bool:
        raw = self.serialize() + secret
        return hashlib.sha256(raw.encode()).hexdigest() == self.signature

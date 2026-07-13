from __future__ import annotations

from typing import Dict, List, Optional

from capability.models import Capability
from capability.versioning import VersionManager


class CapabilityRegistry:
    """
    Unified capability control plane
    """

    def __init__(self):
        self.capabilities: Dict[str, List[Capability]] = {}
        self.version_manager = VersionManager()

    # -------------------------
    # register
    # -------------------------

    def register(self, capability: Capability):
        self.capabilities.setdefault(capability.name, []).append(capability)

    # -------------------------
    # query
    # -------------------------

    def get(self, name: str) -> Optional[Capability]:
        caps = self.capabilities.get(name)
        if not caps:
            return None

        # return latest version
        return sorted(
            caps,
            key=lambda c: c.version.version,
            reverse=True
        )[0]

    def list(self):
        return [
            self.get(name)
            for name in self.capabilities.keys()
        ]

    # -------------------------
    # compatibility resolution
    # -------------------------

    def resolve_all(self):
        all_caps = []

        for caps in self.capabilities.values():
            for c in caps:
                all_caps.append(c)

        return self.version_manager.resolve(all_caps)

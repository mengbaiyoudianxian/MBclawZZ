from __future__ import annotations

import importlib
from typing import Dict

from cap_market.cap_format import CapPackage
from cap_market.registry import CapRegistry


class PackageCenter:
    """
    lifecycle manager for .cap packages
    """

    def __init__(self, registry: CapRegistry):
        self.registry = registry
        self.installed: Dict[str, CapPackage] = {}

    # -----------------------
    # install
    # -----------------------

    def install(self, cap: CapPackage):
        self.registry.publish(cap)
        self.installed[cap.name] = cap

    # -----------------------
    # upgrade
    # -----------------------

    def upgrade(self, cap: CapPackage):
        self.installed[cap.name] = cap
        self.registry.publish(cap)

    # -----------------------
    # uninstall
    # -----------------------

    def uninstall(self, name: str):
        if name in self.installed:
            del self.installed[name]

    # -----------------------
    # runtime loader
    # -----------------------

    def load_entry(self, cap: CapPackage):
        module_path, func_name = cap.entry.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, func_name)

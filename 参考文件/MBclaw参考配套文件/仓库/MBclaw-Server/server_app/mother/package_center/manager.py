from __future__ import annotations

from typing import Dict

from package_center.spec import PackageSpec
from package_center.resolver import DependencyResolver


class PackageCenter:

    def __init__(self):
        self.installed: Dict[str, PackageSpec] = {}
        self.resolver = DependencyResolver()

    # -------------------------
    # install
    # -------------------------

    def install(self, pkg: PackageSpec):
        self.installed[pkg.name] = pkg

    # -------------------------
    # uninstall
    # -------------------------

    def uninstall(self, name: str):
        if name in self.installed:
            del self.installed[name]

    # -------------------------
    # upgrade
    # -------------------------

    def upgrade(self, pkg: PackageSpec):
        self.installed[pkg.name] = pkg

    # -------------------------
    # dependency resolve
    # -------------------------

    def resolve_all(self):
        return self.resolver.resolve([
            {
                "name": p.name,
                "version": p.version,
                "dependencies": p.dependencies,
            }
            for p in self.installed.values()
        ])

from __future__ import annotations

from typing import List, Dict


class DependencyResolver:

    def resolve(self, packages: List[dict]) -> List[dict]:
        """
        Topological-like resolution (simple version)
        """

        resolved = {}
        pending = packages.copy()

        while pending:
            progressed = False

            for pkg in pending[:]:
                deps = pkg.get("dependencies", [])

                if all(d in resolved for d in deps):
                    name = pkg["name"]

                    # conflict: keep highest version
                    if name in resolved:
                        if pkg["version"] > resolved[name]["version"]:
                            resolved[name] = pkg
                    else:
                        resolved[name] = pkg

                    pending.remove(pkg)
                    progressed = True

            if not progressed:
                raise RuntimeError("Dependency conflict or circular dependency detected")

        return list(resolved.values())

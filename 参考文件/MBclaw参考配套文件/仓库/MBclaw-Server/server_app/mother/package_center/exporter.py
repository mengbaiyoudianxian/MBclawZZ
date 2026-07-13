from __future__ import annotations

import json
import zipfile
from typing import List

from package_center.spec import PackageSpec


class PackageExporter:

    def export(self, packages: List[PackageSpec], path: str):

        archive_data = []

        for p in packages:
            archive_data.append({
                "name": p.name,
                "version": p.version,
                "type": p.type,
                "entry": p.entry,
                "dependencies": p.dependencies,
                "permissions": p.permissions,
                "metadata": p.metadata,
                "signature": p.signature,
            })

        with zipfile.ZipFile(path, "w") as z:
            z.writestr("packages.json", json.dumps(archive_data, indent=2))

    def import_archive(self, path: str) -> List[PackageSpec]:

        with zipfile.ZipFile(path, "r") as z:
            data = json.loads(z.read("packages.json"))

        return [
            PackageSpec(
                name=p["name"],
                version=p["version"],
                type=p["type"],
                entry=p["entry"],
                dependencies=p.get("dependencies", []),
                permissions=p.get("permissions", []),
                metadata=p.get("metadata", {}),
                signature=p.get("signature", ""),
            )
            for p in data
        ]

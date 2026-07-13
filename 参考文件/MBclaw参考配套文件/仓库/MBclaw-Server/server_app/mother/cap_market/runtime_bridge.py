from __future__ import annotations

from cap_market.registry import CapRegistry
from cap_market.package_center import PackageCenter
from cap_market.cap_format import CapPackage
from runtime.engine import RuntimeEngine


class MarketplaceRuntimeBridge:

    def __init__(self, runtime: RuntimeEngine):
        self.runtime = runtime

    # -----------------------------
    # pull + install + activate
    # -----------------------------

    def deploy(self, cap: CapPackage):

        # 1. install into marketplace system
        self.runtime.package_center.install(cap)

        # 2. activate into runtime
        entry = self.runtime.install_from_market(cap)

        return {
            "installed": cap.name,
            "version": cap.version,
            "entry_loaded": entry.__name__ if entry else None
        }

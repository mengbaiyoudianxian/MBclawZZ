from runtime.engine import RuntimeEngine
from cap_market.package_center import PackageCenter
from capability.registry import CapabilityRegistry
from cap_market.registry import CapRegistry
from cap_market.runtime_bridge import MarketplaceRuntimeBridge


class MBclaw:

    def __init__(self):

        self.capability_registry = CapabilityRegistry()

        self.package_center = PackageCenter(
            registry=CapRegistry()
        )

        self.engine = RuntimeEngine(
            registry=self.capability_registry,
            package_center=self.package_center
        )

        # NEW: marketplace bridge
        self.market = MarketplaceRuntimeBridge(self.engine)

    def run(self, goal: str, context: dict | None = None):
        return self.engine.run_goal(goal, context or {})

    def install_capability(self, cap):
        """
        runtime dynamic install from marketplace
        """
        return self.market.deploy(cap)

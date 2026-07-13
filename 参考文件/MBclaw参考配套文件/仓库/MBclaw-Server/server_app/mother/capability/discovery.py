from __future__ import annotations

from fastapi import FastAPI
from capability.registry import CapabilityRegistry


class CapabilityDiscoveryAPI:
    """
    REST/GraphQL-style capability discovery
    """

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
        self.app = FastAPI()

        self._register_routes()

    def _register_routes(self):

        @self.app.get("/capabilities")
        def list_capabilities():
            return [
                c.__dict__ if c else None
                for c in self.registry.list()
            ]

        @self.app.get("/capabilities/{name}")
        def get_capability(name: str):
            cap = self.registry.get(name)
            return cap.__dict__ if cap else None

        @self.app.get("/capabilities/version/resolved")
        def resolved():
            return self.registry.resolve_all()

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ProviderKey:
    key: str
    active: bool = True
    weight: float = 1.0


@dataclass
class Provider:
    name: str
    base_url: str
    cost_per_1k: float

    keys: List[ProviderKey] = field(default_factory=list)


class ProviderRegistry:
    """
    Stores all LLM providers + API keys.
    """

    def __init__(self):
        self.providers: Dict[str, Provider] = {}

    def register(self, provider: Provider):
        self.providers[provider.name] = provider

    def get(self, name: str) -> Provider:
        return self.providers[name]

    def list(self):
        return list(self.providers.values())

    def rotate_key(self, provider_name: str):
        p = self.providers[provider_name]
        if not p.keys:
            return None

        # simple round-robin rotation
        key = p.keys.pop(0)
        p.keys.append(key)
        return key

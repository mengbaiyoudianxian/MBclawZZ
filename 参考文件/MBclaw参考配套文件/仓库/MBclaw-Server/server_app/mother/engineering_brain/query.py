from __future__ import annotations

from typing import List


class EngineeringBrainQuery:

    def __init__(self, registry):

        self.registry = registry

    # -------------------------
    # worker bootstrap read
    # -------------------------

    def bootstrap_context(self):

        return self.registry.get_context()

    # -------------------------
    # query by module
    # -------------------------

    def query_module(self, module: str):

        debts = [
            d for d in self.registry.debts.values()
            if d.module == module
        ]

        knowledge = [
            k for k in self.registry.knowledge.values()
            if module in (k.tags or [])
        ]

        return {
            "debts": debts,
            "knowledge": knowledge
        }

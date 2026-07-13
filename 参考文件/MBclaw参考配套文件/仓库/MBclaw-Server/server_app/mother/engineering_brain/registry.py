from __future__ import annotations

from typing import Dict, List, Any


class EngineeringRegistry:

    def __init__(self):

        self.adrs: Dict[str, Any] = {}
        self.knowledge: Dict[str, Any] = {}
        self.debts: Dict[str, Any] = {}

    # -------------------------
    # write ADR
    # -------------------------

    def add_adr(self, adr):

        self.adrs[adr.id] = adr

    # -------------------------
    # write knowledge
    # -------------------------

    def add_knowledge(self, k):

        self.knowledge[k.id] = k

    # -------------------------
    # write tech debt
    # -------------------------

    def add_debt(self, d):

        self.debts[d.id] = d

    # -------------------------
    # query interface
    # -------------------------

    def get_context(self):

        return {
            "adrs": list(self.adrs.values()),
            "knowledge": list(self.knowledge.values()),
            "debts": list(self.debts.values())
        }

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .enums import ActionType, RiskLevel


@dataclass
class RiskScore:
    total: int
    level: RiskLevel
    breakdown: Dict[str, int]


class RiskEngine:
    """
    Converts action + context into normalized risk score.
    """

    def __init__(self):
        self.weights = {
            ActionType.READ: 1,
            ActionType.WRITE: 3,
            ActionType.EXECUTE: 5,
            ActionType.DELETE: 7,
            ActionType.NETWORK: 6,
            ActionType.TOOL_CALL: 4,
            ActionType.SYSTEM: 9,
        }

    def score_action(self, action: Dict[str, Any]) -> RiskScore:
        base_type = action.get("type")
        payload = action.get("payload", {})

        weight = self.weights.get(base_type, 1)

        modifiers = 0
        breakdown = {"base": weight}

        # heuristic modifiers
        if payload.get("destructive"):
            modifiers += 3
            breakdown["destructive"] = 3

        if payload.get("external_network"):
            modifiers += 2
            breakdown["network"] = 2

        if payload.get("writes_state"):
            modifiers += 2
            breakdown["state_change"] = 2

        total = weight + modifiers

        level = self._map_level(total)

        return RiskScore(
            total=total,
            level=level,
            breakdown=breakdown,
        )

    def score_proposal(self, proposal: Dict[str, Any]) -> RiskScore:
        total = 0
        breakdown = {}

        for i, action in enumerate(proposal.get("actions", [])):
            r = self.score_action(action)
            total += r.total
            breakdown[f"action_{i}"] = r.total

        level = self._map_level(total)

        return RiskScore(
            total=total,
            level=level,
            breakdown=breakdown,
        )

    def _map_level(self, score: int) -> RiskLevel:
        if score <= 3:
            return RiskLevel.LOW
        if score <= 7:
            return RiskLevel.MEDIUM
        if score <= 12:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

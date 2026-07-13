import pytest

from governor.governor import Governor
from governor.models import Proposal, Action, ContextState
from governor.enums import ActionType


def test_allow_simple_read():
    gov = Governor()

    proposal = Proposal(
        actions=[
            Action(
                type=ActionType.READ,
                name="read_file",
                payload={},
            )
        ],
        context=ContextState(),
    )

    decision = gov.evaluate(proposal)

    assert decision is not None


def test_risk_increases():
    gov = Governor()

    proposal = Proposal(
        actions=[
            Action(
                type=ActionType.DELETE,
                name="delete_data",
                payload={"destructive": True},
            )
        ],
        context=ContextState(),
    )

    decision = gov.evaluate(proposal)

    assert decision.final_risk.value >= 2


def test_blacklisted_action():
    gov = Governor()

    proposal = Proposal(
        actions=[
            Action(
                type=ActionType.SYSTEM,
                name="self_modify_kernel",
                payload={},
            )
        ],
        context=ContextState(),
    )

    decision = gov.evaluate(proposal)

    assert decision.status.value in ["rejected", "review"]

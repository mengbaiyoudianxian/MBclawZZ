from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .governor import Governor
from .models import Action, Proposal, ContextState
from .executor import Executor


app = FastAPI(title="Governor API")

governor = Governor()
executor = Executor()


class ActionRequest(BaseModel):
    type: str
    name: str
    payload: dict = {}


class ExecuteRequest(BaseModel):
    actions: list[ActionRequest]


@app.post("/evaluate")
def evaluate(req: ExecuteRequest):
    actions = [
        Action(
            type=a.type,
            name=a.name,
            payload=a.payload,
        )
        for a in req.actions
    ]

    proposal = Proposal(
        actions=actions,
        context=ContextState(),
        rationale="api_eval",
    )

    decision = governor.evaluate(proposal)

    return decision.model_dump()


@app.post("/execute")
def execute(req: ExecuteRequest):
    actions = [
        Action(
            type=a.type,
            name=a.name,
            payload=a.payload,
        )
        for a in req.actions
    ]

    proposal = Proposal(
        actions=actions,
        context=ContextState(),
        rationale="api_exec",
    )

    decision = governor.evaluate(proposal)

    if decision.status.value != "approved":
        return {
            "status": "blocked",
            "reason": decision.reason,
        }

    results = []
    for action in actions:
        results.append(executor.run(action))

    return {
        "status": "ok",
        "results": results,
    }

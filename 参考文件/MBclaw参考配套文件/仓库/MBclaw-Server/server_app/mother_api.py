from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server_app.mother.unified_runtime import get_runtime

router = APIRouter(prefix="/api/mother/runtime", tags=["mother-runtime"])


class GoalRequest(BaseModel):
    goal: str = Field(min_length=1)
    context: dict = Field(default_factory=dict)


@router.get("/status")
def mother_runtime_status():
    return get_runtime().status()


@router.post("/plan")
def mother_runtime_plan(req: GoalRequest):
    plan = get_runtime().create_plan(req.goal, req.context)
    return get_runtime().status()["plan"]


@router.post("/run")
def mother_runtime_run(req: GoalRequest):
    return get_runtime().run_goal(req.goal, req.context)


@router.post("/run-current")
def mother_runtime_run_current():
    try:
        return get_runtime().run_plan()
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.get("/events")
def mother_runtime_events(limit: int = 50):
    return {"events": get_runtime().bus.recent(limit)}

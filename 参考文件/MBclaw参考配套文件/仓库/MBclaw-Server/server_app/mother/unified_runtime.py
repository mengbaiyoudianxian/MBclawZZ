from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from server_app.mother.config import config
from server_app.mother.config import config
from server_app.mother.governor.enums import ActionType, RiskLevel
from server_app.mother.governor.governor import Governor
from server_app.mother.governor.models import Action, ContextState, Proposal
from server_app.mother.planner.decomposer import TaskDecomposer
from server_app.mother.planner.models import Plan, Task
from server_app.mother.planner.replanner import RePlanner
from server_app.mother.runtime.persistence import StateStore


@dataclass
class RuntimeEvent:
    event_id: str
    type: str
    payload: dict[str, Any]
    ts: float = field(default_factory=time.time)


class UnifiedEventBus:
    def __init__(self, max_events: int = 500):
        self.max_events = max_events
        self.events: list[RuntimeEvent] = []
        self.subscribers: dict[str, list] = {}

    def emit(self, event_type: str, payload: dict[str, Any]) -> RuntimeEvent:
        event = RuntimeEvent(uuid.uuid4().hex[:12], event_type, payload)
        self.events.append(event)
        self.events = self.events[-self.max_events:]
        for callback in self.subscribers.get(event_type, []):
            callback(payload)
        for key, callbacks in self.subscribers.items():
            if key.endswith("*") and event_type.startswith(key[:-1]):
                for callback in callbacks:
                    callback(payload)
        return event

    def subscribe(self, event_type: str, callback):
        self.subscribers.setdefault(event_type, []).append(callback)

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        return [asdict(e) for e in self.events[-limit:]]


class UnifiedScheduler:
    def __init__(self):
        self.queue: list[Task] = []

    def load_plan(self, plan: Plan):
        completed = {t.task_id for t in plan.tasks if t.status == "done"}
        failed = {t.task_id for t in plan.tasks if t.status == "failed"}
        self.queue = [t for t in plan.tasks if t.status == "pending" and t.task_id not in completed and t.task_id not in failed]
        self.queue.sort(key=lambda t: (-t.priority, t.estimated_cost, t.name))

    def next_task(self) -> Task | None:
        if not self.queue:
            return None
        return self.queue.pop(0)

    def snapshot(self) -> list[dict[str, Any]]:
        return [asdict(t) for t in self.queue]


class UnifiedWorker:
    def execute(self, task: Task) -> dict[str, Any]:
        outputs = {}
        capabilities = task.required_capabilities or ["reasoning"]
        for capability in capabilities:
            outputs[capability] = {
                "ok": True,
                "message": f"capability '{capability}' executed for task '{task.name}'",
            }
        task.outputs = outputs
        task.status = "done"
        return {"task_id": task.task_id, "task": task.name, "outputs": outputs}


class UnifiedMotherRuntime:
    def __init__(self, db_path: str | None = None, max_replans: int | None = None, max_iterations: int | None = None):
        db_path = db_path or config.runtime_db
        max_replans = config.max_replans if max_replans is None else max_replans
        max_iterations = config.max_iterations if max_iterations is None else max_iterations
        self.bus = UnifiedEventBus()
        self.decomposer = TaskDecomposer()
        self.replanner = RePlanner()
        self.scheduler = UnifiedScheduler()
        self.worker = UnifiedWorker()
        self.governor = Governor()
        self.store = StateStore(db_path)
        self.max_replans = max_replans
        self.max_iterations = max_iterations
        self.current_plan: Plan | None = None
        self.running = False

    def create_plan(self, goal: str, context: dict[str, Any] | None = None) -> Plan:
        plan = self.decomposer.decompose(goal, context or {})
        self.current_plan = plan
        self.scheduler.load_plan(plan)
        self._persist()
        self.bus.emit("plan.created", {"plan_id": plan.plan_id, "goal": goal, "tasks": len(plan.tasks)})
        return plan

    def run_goal(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        plan = self.create_plan(goal, context)
        return self.run_plan(plan)

    def run_plan(self, plan: Plan | None = None) -> dict[str, Any]:
        plan = plan or self.current_plan
        if not plan:
            raise ValueError("no plan loaded")
        self.current_plan = plan
        self.scheduler.load_plan(plan)
        self.running = True
        results = []
        errors = []
        replan_counts: dict[str, int] = {}
        iterations = 0
        self.bus.emit("runtime.started", {"plan_id": plan.plan_id})
        while iterations < self.max_iterations:
            iterations += 1
            task = self.scheduler.next_task()
            if not task:
                break
            task.status = "running"
            self.bus.emit("task.started", {"task_id": task.task_id, "name": task.name})
            try:
                decision = self.governor.evaluate(self._proposal_for_task(task, plan))
                if decision.status.value != "approved":
                    task.status = "blocked"
                    errors.append({"task_id": task.task_id, "error": decision.reason or decision.status.value})
                    self.bus.emit("task.blocked", {"task_id": task.task_id, "reason": decision.reason})
                    continue
                result = self.worker.execute(task)
                results.append(result)
                self.bus.emit("task.completed", result)
            except Exception as exc:
                task.status = "failed"
                errors.append({"task_id": task.task_id, "error": str(exc)})
                self.bus.emit("task.failed", {"task_id": task.task_id, "error": str(exc)})
                base = task.name.replace("recover_", "")
                replan_counts[base] = replan_counts.get(base, 0) + 1
                if replan_counts[base] <= self.max_replans:
                    plan = self.replanner.replan(plan, task.task_id, str(exc))
                    for t in plan.tasks:
                        if t.name.startswith("recover_recover_"):
                            t.name = t.name.replace("recover_recover_", "recover_", 1)
                    self.current_plan = plan
                    self.scheduler.load_plan(plan)
                    self.bus.emit("plan.replanned", {"plan_id": plan.plan_id, "failed_task_id": task.task_id, "version": plan.version})
                else:
                    self.bus.emit("plan.replan_skipped", {"task_id": task.task_id, "reason": "max_replans_reached"})
        self.running = False
        plan.status = "completed" if not self.scheduler.queue and not errors else "partial"
        self._persist()
        summary = {
            "plan_id": plan.plan_id,
            "status": plan.status,
            "iterations": iterations,
            "results": results,
            "errors": errors,
            "events": self.bus.recent(20),
        }
        self.bus.emit("runtime.completed", {"plan_id": plan.plan_id, "status": plan.status, "iterations": iterations})
        return summary

    def status(self) -> dict[str, Any]:
        plan = self.current_plan
        return {
            "running": self.running,
            "plan": self._plan_dict(plan) if plan else None,
            "queue": self.scheduler.snapshot(),
            "events": self.bus.recent(50),
            "limits": {"max_replans": self.max_replans, "max_iterations": self.max_iterations},
        }

    def _proposal_for_task(self, task: Task, plan: Plan) -> Proposal:
        action_type = ActionType.TOOL_CALL
        if any(c in ("code_edit", "write", "integration") for c in task.required_capabilities):
            action_type = ActionType.WRITE
        if any(c in ("system", "shell") for c in task.required_capabilities):
            action_type = ActionType.EXECUTE
        action = Action(
            type=action_type,
            name=task.name,
            payload={
                "task_id": task.task_id,
                "capabilities": task.required_capabilities,
                "writes_state": action_type in (ActionType.WRITE, ActionType.EXECUTE),
            },
            risk_hint=RiskLevel.LOW,
        )
        return Proposal(
            actions=[action],
            context=ContextState(session_id=plan.plan_id, variables=plan.context),
            rationale=f"Execute planned task '{task.name}' for goal '{plan.goal}'",
            tags=["mother_runtime", "planner", "governor"],
        )

    def _persist(self):
        if self.current_plan:
            self.store.set("current_plan", self._plan_dict(self.current_plan))
        self.store.set("events", {"items": self.bus.recent(200)})

    def _plan_dict(self, plan: Plan) -> dict[str, Any]:
        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "context": plan.context,
            "version": plan.version,
            "status": plan.status,
            "tasks": [asdict(t) for t in plan.tasks],
        }


_runtime: UnifiedMotherRuntime | None = None


def get_runtime() -> UnifiedMotherRuntime:
    global _runtime
    if _runtime is None:
        _runtime = UnifiedMotherRuntime()
    return _runtime

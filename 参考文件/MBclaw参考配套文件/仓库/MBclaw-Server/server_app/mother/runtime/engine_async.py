from __future__ import annotations

import asyncio
from typing import Any, Dict

from runtime.state import RuntimeState, RuntimeStatus
from runtime.worker import Worker
from runtime.dispatcher import Dispatcher
from runtime.async_worker_pool import AsyncWorkerPool
from runtime.event_bus import EventBus
from runtime.trace import TraceLogger
from runtime.persistence import StateStore

from scheduler.scheduler import Scheduler
from planner.planner import Planner
from governor.governor import Governor


class AsyncRuntimeEngine:
    """
    Production-grade MBclaw kernel (async version).
    """

    def __init__(self):
        self.state = RuntimeState()

        self.store = StateStore()
        self.events = EventBus()
        self.trace = TraceLogger()

        self.planner = Planner()
        self.scheduler = Scheduler()
        self.governor = Governor()

        self.worker = Worker(registry=None)  # can inject registry later
        self.pool = AsyncWorkerPool(self.worker)

    # -------------------------
    # Entry
    # -------------------------

    async def run_goal(self, goal: str, context: dict):
        self.state.status = RuntimeStatus.RUNNING

        self.events.publish("goal_started", {"goal": goal})
        self.trace.log("goal_started", {"goal": goal})

        plan = self.planner.create_plan(goal, context)
        self.scheduler.load_plan(plan)

        tasks = []

        while True:
            task = self.scheduler.next_task()
            if not task:
                break

            decision = self.governor.evaluate(
                self._task_to_proposal(task)
            )

            if decision.status.value != "approved":
                self.trace.log("task_blocked", {"task": task.task_id})
                continue

            tasks.append(task)

        results = await self.pool.run_batch(tasks)

        self.state.status = RuntimeStatus.STOPPED

        self.store.set("last_run", {
            "goal": goal,
            "result_count": len(results),
        })

        self.events.publish("goal_finished", {"results": len(results)})
        self.trace.log("goal_finished", {"count": len(results)})

        return results

    # -------------------------
    # Adapter
    # -------------------------

    def _task_to_proposal(self, task):
        from governor.models import Proposal, Action, ContextState
        from governor.enums import ActionType

        action = Action(
            type=ActionType.TOOL_CALL,
            name=task.name,
            payload={
                "inputs": task.inputs,
                "caps": task.required_capabilities,
            },
        )

        return Proposal(
            actions=[action],
            context=ContextState(),
            rationale="async_runtime_gate",
        )

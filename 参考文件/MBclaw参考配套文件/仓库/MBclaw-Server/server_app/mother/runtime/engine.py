from __future__ import annotations

from runtime.state import RuntimeState, RuntimeStatus
from planner.planner import Planner
from scheduler.scheduler import Scheduler
from runtime.dispatcher import Dispatcher
from runtime.worker import Worker
from capability.registry import CapabilityRegistry
from governor.governor import Governor

# NEW
from cap_market.package_center import PackageCenter
from cap_market.registry import CapRegistry
from cap_market.cap_format import CapPackage


class RuntimeEngine:

    def __init__(self,
                 registry: CapabilityRegistry,
                 package_center: PackageCenter):

        self.state = RuntimeState()

        self.registry = registry
        self.package_center = package_center

        self.worker = Worker(self.registry)
        self.scheduler = Scheduler()
        self.dispatcher = Dispatcher(self.scheduler)

        self.planner = Planner()
        self.governor = Governor()

        self.plan = None

    # -----------------------------
    # NEW: marketplace install hook
    # -----------------------------

    def install_from_market(self, cap: CapPackage):
        """
        Install capability at runtime
        """

        self.package_center.install(cap)

        # auto register into runtime capability system
        entry_func = self.package_center.load_entry(cap)

        from capability.models import Capability, CapabilityIO, CapabilityVersion

        capability = Capability(
            name=cap.name,
            type="market_skill",
            description=cap.description,

            inputs=[],
            outputs=[],

            permission="medium",

            mcp_mapping=None,

            version=CapabilityVersion(cap.version),
        )

        self.registry.register(capability)

        return entry_func

    # -----------------------------
    # main runtime loop
    # -----------------------------

    def run_goal(self, goal: str, context: dict):

        self.state.status = RuntimeStatus.RUNNING

        self.plan = self.planner.create_plan(goal, context)
        self.scheduler.load_plan(self.plan)

        results = []

        while True:
            task = self.dispatcher.get_next_task()
            if not task:
                break

            try:
                decision = self.governor.evaluate(
                    self._to_proposal(task)
                )

                if decision.status.value != "approved":
                    continue

                result = self.worker.execute(task)

                results.append(result)

                self.state.completed_tasks.append(task.task_id)

            except Exception:
                self.state.failed_tasks.append(task.task_id)

                self.plan = self.planner.handle_failure(
                    self.plan,
                    task.task_id,
                    "runtime error"
                )

                self.scheduler.load_plan(self.plan)

        self.state.status = RuntimeStatus.STOPPED

        return results

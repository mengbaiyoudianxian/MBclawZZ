from __future__ import annotations

from gateway.message import UnifiedMessage


class Dispatcher:

    def __init__(self, planner, worker, governor):

        self.planner = planner
        self.worker = worker
        self.governor = governor

    # -----------------------------
    # routing core
    # -----------------------------

    def dispatch(self, msg: UnifiedMessage):

        # command -> worker
        if msg.type == "command":
            return self._to_worker(msg)

        # text -> planner (default enters task system)
        if msg.type == "text":
            return self._to_planner(msg)

        # event / image -> governor review
        return self._to_governor(msg)

    def _to_worker(self, msg):
        return self.worker.execute(msg.content)

    def _to_planner(self, msg):
        plan = self.planner.create_plan(msg.content, context={"user": msg.user_id})
        return plan

    def _to_governor(self, msg):
        decision = self.governor.evaluate(msg)
        return decision

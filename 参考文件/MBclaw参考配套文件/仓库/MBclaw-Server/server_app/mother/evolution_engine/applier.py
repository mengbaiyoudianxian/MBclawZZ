from __future__ import annotations


class EvolutionApplier:

    def apply(self, prt: dict, scheduler=None, token_pool=None, workflow_engine=None):

        if prt["type"] == "scheduler_adjustment":
            if scheduler:
                scheduler.switch_model(prt["target"], "fast")

        elif prt["type"] == "token_optimization":
            if token_pool:
                token_pool.enable_compression(prt["target"])

        elif prt["type"] == "workflow_restructure":
            if workflow_engine:
                workflow_engine.add_fallback(prt["target"])

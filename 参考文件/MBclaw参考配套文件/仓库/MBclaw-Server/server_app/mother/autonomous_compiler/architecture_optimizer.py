class ArchitectureOptimizer:

    def optimize(self, system_ir):

        optimized = system_ir

        # prune high-failure modules
        for module in list(optimized.modules.keys()):

            meta = optimized.modules[module]

            if getattr(meta, "failure_rate", 0) > 0.3:
                del optimized.modules[module]

        return optimized

from __future__ import annotations

from mutation.mutation_store import MutationStore
from mutation.kernel_analyzer import KernelAnalyzer
from mutation.governor_layer import MutationGovernor
from memory_engine_v2.memory_engine import MemoryEngineV2


class SelfModifyingKernel:

    def __init__(self, memory: MemoryEngineV2):

        self.memory = memory

        self.store = MutationStore()
        self.analyzer = KernelAnalyzer()
        self.governor = MutationGovernor()

    # -----------------------------
    # main loop: generate + review + apply
    # -----------------------------

    def evolve(self):

        memories = self.memory.store.all()

        candidates = self.analyzer.extract_mutations(memories)

        for m in candidates:

            if self.governor.evaluate(m):
                self.store.propose(m)
                self.store.apply(m)

        return self.store.active_state

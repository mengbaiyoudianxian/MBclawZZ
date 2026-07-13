from __future__ import annotations

from typing import List, Dict
from mutation.mutation_spec import MutationSpec


class MutationStore:

    def __init__(self):
        self.history: List[MutationSpec] = []
        self.active_state: Dict[str, Dict] = {}

    def propose(self, mutation: MutationSpec):
        self.history.append(mutation)

    def apply(self, mutation: MutationSpec):

        if mutation.target not in self.active_state:
            self.active_state[mutation.target] = {}

        self.active_state[mutation.target].update(mutation.patch)

        mutation.status = "applied"

    def rollback(self, mutation_id: str):

        for m in reversed(self.history):
            if m.id == mutation_id:

                # naive rollback: remove patch
                for k in m.patch.keys():
                    self.active_state[m.target].pop(k, None)

                m.status = "rejected"
                return True

        return False

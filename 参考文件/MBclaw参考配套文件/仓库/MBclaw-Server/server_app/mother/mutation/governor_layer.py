from __future__ import annotations

from mutation.mutation_spec import MutationSpec


class MutationGovernor:

    def evaluate(self, mutation: MutationSpec) -> bool:

        # risk control core rules

        if mutation.confidence < 0.6:
            return False

        if mutation.type not in ["policy", "routing", "memory"]:
            return False

        # disallow oversized patches
        if len(mutation.patch) > 5:
            return False

        return True

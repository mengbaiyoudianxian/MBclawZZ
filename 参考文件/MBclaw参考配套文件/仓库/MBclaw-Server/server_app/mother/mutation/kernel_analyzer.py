from __future__ import annotations

from typing import List
from memory_engine_v2.memory_schema import MemoryRecord
from mutation.mutation_spec import MutationSpec
import uuid


class KernelAnalyzer:

    def extract_mutations(self, memories: List[MemoryRecord]) -> List[MutationSpec]:

        mutations = []

        for m in memories:

            # repeated failure -> reduce policy weight
            if m.success is False and m.access_count > 3:

                mutations.append(MutationSpec(
                    id=str(uuid.uuid4()),
                    type="policy",
                    target="retrieval_policy",
                    patch={"failure_penalty": 0.2},
                    reason="repeated failure pattern",
                    confidence=0.7
                ))

            # high success -> reinforce path
            if m.success is True and m.importance > 0.7:

                mutations.append(MutationSpec(
                    id=str(uuid.uuid4()),
                    type="policy",
                    target="routing_policy",
                    patch={"success_bias": 0.15},
                    reason="high success reinforcement",
                    confidence=0.8
                ))

        return mutations

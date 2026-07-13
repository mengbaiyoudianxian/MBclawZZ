from __future__ import annotations

from typing import List

from .execution_snapshot import ExecutionSnapshot


class ReplayEngine:
    """
    Deterministic replay of execution traces.
    """

    def __init__(self):
        self.snapshots: List[ExecutionSnapshot] = []

    def record(self, snapshot: ExecutionSnapshot):
        self.snapshots.append(snapshot.clone())

    def replay(self):
        results = []

        for snap in self.snapshots:
            results.append({
                "state": snap.state,
                "tasks": len(snap.tasks),
            })

        return results

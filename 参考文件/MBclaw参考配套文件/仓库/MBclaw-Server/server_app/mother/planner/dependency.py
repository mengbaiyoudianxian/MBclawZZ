from __future__ import annotations

from typing import List

from .models import Plan


class DependencyResolver:
    """
    Builds execution order from task graph.
    """

    def resolve(self, plan: Plan) -> List[str]:
        task_map = {t.task_id: t for t in plan.tasks}

        resolved = []
        visited = set()

        def visit(task_id: str):
            if task_id in visited:
                return

            task = task_map.get(task_id)
            if not task:
                return

            for dep in task.dependencies:
                visit(dep)

            visited.add(task_id)
            resolved.append(task_id)

        for t in plan.tasks:
            visit(t.task_id)

        return resolved

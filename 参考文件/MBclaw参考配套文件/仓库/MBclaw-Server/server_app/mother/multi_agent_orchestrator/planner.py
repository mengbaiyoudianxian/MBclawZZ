import uuid


class DAGPlanner:

    def plan(self, goal: str):

        if "build" in goal:

            return [
                {
                    "id": str(uuid.uuid4()),
                    "task": "design architecture",
                    "agent": "claude",
                    "deps": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "task": "implement core logic",
                    "agent": "deepseek",
                    "deps": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "task": "ui generation",
                    "agent": "doubao",
                    "deps": []
                }
            ]

        return [
            {
                "id": str(uuid.uuid4()),
                "task": goal,
                "agent": "deepseek",
                "deps": []
            }
        ]

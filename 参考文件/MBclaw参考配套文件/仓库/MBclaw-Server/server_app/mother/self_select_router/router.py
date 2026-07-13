from self_select_router.agent_registry import AgentRegistry
from self_select_router.task_analyzer import TaskAnalyzer
from self_select_router.cost_model import CostModel


class ToolRouter:

    def __init__(self):

        self.registry = AgentRegistry()
        self.analyzer = TaskAnalyzer()
        self.cost_model = CostModel()

    # -------------------------
    # core routing decision
    # -------------------------

    def route(self, task: str):

        task_type = self.analyzer.analyze(task)

        scored = []

        for agent in self.registry.agents.values():

            score = self.cost_model.score(agent, task_type)

            scored.append((agent, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        best_agent = scored[0][0]

        return {
            "selected_agent": best_agent.name,
            "task_type": task_type,
            "tool_stack": best_agent.tool_stack
        }

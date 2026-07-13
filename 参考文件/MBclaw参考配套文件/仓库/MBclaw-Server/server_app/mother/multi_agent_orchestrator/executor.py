from typing import Dict


class Executor:

    def __init__(self, agent_pool):

        self.agent_pool = agent_pool

    def execute(self, tasks: Dict):

        results = {}

        for t in tasks:

            agent = self.agent_pool.agents.get(t["agent"])

            if agent:
                results[t["id"]] = agent(t["task"])

        return results

class CostModel:

    def score(self, agent, task_type):

        base = 0

        if task_type in agent.strengths:
            base += 0.6

        base += agent.reliability * 0.2
        base += agent.speed * 0.2
        base -= agent.cost_level * 0.3

        return base

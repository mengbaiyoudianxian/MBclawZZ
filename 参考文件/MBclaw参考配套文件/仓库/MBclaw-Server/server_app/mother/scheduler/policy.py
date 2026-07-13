class RoutingPolicy:

    def select_candidates(self, task_type: str):
        if task_type in ["code", "tool"]:
            return ["claude", "gpt-4.1", "deepseek"]
        if task_type in ["chat", "reasoning"]:
            return ["gpt-4o", "claude", "deepseek"]
        if task_type in ["cheap", "bulk"]:
            return ["deepseek", "local"]
        return ["gpt-4o", "claude"]

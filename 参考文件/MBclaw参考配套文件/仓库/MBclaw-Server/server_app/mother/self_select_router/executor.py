class ExecutionEngine:

    def execute(self, route_result: dict, task: str):

        agent = route_result["selected_agent"]

        tool_stack = route_result["tool_stack"]

        return {
            "agent": agent,
            "tools_used": tool_stack,
            "result": f"Executed {task} using {agent}"
        }

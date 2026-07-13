class ToolExecutor:

    def execute(self, tool_name, payload):

        return {
            "tool": tool_name,
            "input": payload,
            "output": f"executed {tool_name}"
        }

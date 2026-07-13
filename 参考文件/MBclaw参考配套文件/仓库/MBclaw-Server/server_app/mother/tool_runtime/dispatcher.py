from tool_runtime.executors.subprocess_executor import SubprocessExecutor
from tool_runtime.executors.http_executor import HTTPExecutor
from tool_runtime.executors.browser_executor import BrowserExecutor
from tool_runtime.executors.sandbox_executor import SandboxExecutor
from tool_runtime.types import ToolCall
from tool_runtime.context import ExecutionContext


class ToolDispatcher:

    def __init__(self, eventbus=None):
        self.executors = {
            "subprocess": SubprocessExecutor(eventbus),
            "http": HTTPExecutor(eventbus),
            "browser": BrowserExecutor(eventbus),
            "sandbox": SandboxExecutor(eventbus),
        }

    def resolve_executor(self, tool_call: ToolCall):
        t = tool_call.args.get("type", "subprocess")
        return self.executors.get(t, self.executors["subprocess"])

    async def execute(self, tool_call: ToolCall, context: ExecutionContext):
        executor = self.resolve_executor(tool_call)

        if executor.eventbus:
            await executor._emit("tool.called", {
                "tool": tool_call.tool_name,
                "args": tool_call.args
            })

        result = await executor.execute(tool_call, context)

        if executor.eventbus:
            await executor._emit("tool.completed", {
                "tool": tool_call.tool_name,
                "success": result.success,
                "latency": result.latency
            })

        return result

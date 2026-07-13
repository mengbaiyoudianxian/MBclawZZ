import time
import asyncio
from tool_runtime.base import ToolExecutor
from tool_runtime.types import ToolCall, ToolResult
from tool_runtime.context import ExecutionContext


class SandboxExecutor(ToolExecutor):

    async def execute(self, tool_call: ToolCall, context: ExecutionContext) -> ToolResult:
        start = time.time()

        code = tool_call.args.get("code", "print('hello sandbox')")

        try:
            proc = await asyncio.create_subprocess_exec(
                "python3",
                "-c",
                code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await proc.communicate()

            return ToolResult(
                tool_name=tool_call.tool_name,
                success=(proc.returncode == 0),
                output=stdout.decode().strip(),
                error=stderr.decode().strip() or None,
                latency=time.time() - start,
                trace_id=context.trace_id
            )

        except Exception as e:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=str(e),
                latency=time.time() - start,
                trace_id=context.trace_id
            )

import asyncio
import time
from tool_runtime.base import ToolExecutor
from tool_runtime.types import ToolCall, ToolResult
from tool_runtime.context import ExecutionContext


class SubprocessExecutor(ToolExecutor):

    async def execute(self, tool_call: ToolCall, context: ExecutionContext) -> ToolResult:
        start = time.time()

        try:
            cmd = tool_call.args.get("cmd", "echo hello")

            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=tool_call.timeout)

            output = stdout.decode().strip()
            error = stderr.decode().strip()

            return ToolResult(
                tool_name=tool_call.tool_name,
                success=(proc.returncode == 0),
                output=output,
                error=error if error else None,
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

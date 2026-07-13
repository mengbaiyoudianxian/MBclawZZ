import aiohttp
import time
from tool_runtime.base import ToolExecutor
from tool_runtime.types import ToolCall, ToolResult
from tool_runtime.context import ExecutionContext


class HTTPExecutor(ToolExecutor):

    async def execute(self, tool_call: ToolCall, context: ExecutionContext) -> ToolResult:
        start = time.time()

        url = tool_call.args.get("url")
        method = tool_call.args.get("method", "GET")
        payload = tool_call.args.get("data", None)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, json=payload, timeout=tool_call.timeout) as resp:
                    data = await resp.text()

            return ToolResult(
                tool_name=tool_call.tool_name,
                success=True,
                output=data,
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

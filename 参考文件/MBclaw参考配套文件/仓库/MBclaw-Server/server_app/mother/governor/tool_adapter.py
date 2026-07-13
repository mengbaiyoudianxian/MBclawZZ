# tool_adapter.py
# Tool Execution Adapter Layer
# 作用：统一 Capability → ToolExecutor → Runtime 执行链

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Callable


@dataclass
class ToolCall:
    tool_name: str
    args: Dict[str, Any]
    trace_id: str
    task_id: str


@dataclass
class ToolResult:
    success: bool
    output: Any
    error: Optional[str]
    latency: float
    executor_type: str


class ToolExecutor:
    """
    所有执行器统一接口
    """

    async def execute(self, call: ToolCall) -> ToolResult:
        raise NotImplementedError


class SubprocessExecutor(ToolExecutor):
    async def execute(self, call: ToolCall) -> ToolResult:
        start = time.time()
        try:
            await asyncio.sleep(0.1)
            return ToolResult(
                success=True,
                output=f"subprocess executed {call.tool_name}",
                error=None,
                latency=time.time() - start,
                executor_type="subprocess",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                latency=time.time() - start,
                executor_type="subprocess",
            )


class HTTPExecutor(ToolExecutor):
    async def execute(self, call: ToolCall) -> ToolResult:
        start = time.time()
        try:
            await asyncio.sleep(0.05)
            return ToolResult(
                success=True,
                output={"http": "ok", "tool": call.tool_name},
                error=None,
                latency=time.time() - start,
                executor_type="http",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                latency=time.time() - start,
                executor_type="http",
            )


class BrowserExecutor(ToolExecutor):
    async def execute(self, call: ToolCall) -> ToolResult:
        start = time.time()
        try:
            await asyncio.sleep(0.2)
            return ToolResult(
                success=True,
                output={"browser_action": call.args},
                error=None,
                latency=time.time() - start,
                executor_type="browser",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                latency=time.time() - start,
                executor_type="browser",
            )


class SandboxExecutor(ToolExecutor):
    async def execute(self, call: ToolCall) -> ToolResult:
        start = time.time()
        try:
            await asyncio.sleep(0.15)
            return ToolResult(
                success=True,
                output="sandbox result",
                error=None,
                latency=time.time() - start,
                executor_type="sandbox",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                latency=time.time() - start,
                executor_type="sandbox",
            )


class ToolExecutorRouter:
    """
    根据 capability / tool metadata 选择执行器
    """

    def __init__(self):
        self.executors: Dict[str, ToolExecutor] = {
            "subprocess": SubprocessExecutor(),
            "http": HTTPExecutor(),
            "browser": BrowserExecutor(),
            "sandbox": SandboxExecutor(),
        }

    def get_executor(self, tool_type: str) -> ToolExecutor:
        if tool_type not in self.executors:
            raise ValueError(f"Unknown executor type: {tool_type}")
        return self.executors[tool_type]

    async def execute(self, tool_type: str, call: ToolCall) -> ToolResult:
        executor = self.get_executor(tool_type)
        return await executor.execute(call)

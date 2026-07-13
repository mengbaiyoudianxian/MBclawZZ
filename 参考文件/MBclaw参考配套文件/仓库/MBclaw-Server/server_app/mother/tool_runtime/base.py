from abc import ABC, abstractmethod
from tool_runtime.types import ToolCall, ToolResult
from tool_runtime.context import ExecutionContext


class ToolExecutor(ABC):

    def __init__(self, eventbus=None):
        self.eventbus = eventbus

    @abstractmethod
    async def execute(self, tool_call: ToolCall, context: ExecutionContext) -> ToolResult:
        pass

    async def _emit(self, event_type: str, payload: dict):
        if self.eventbus:
            await self.eventbus.publish(event_type, payload)

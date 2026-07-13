from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]
    dangerous: bool = False


class ToolRegistry:
    """
    Central tool registry controlled by Governor.
    """

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)

    def execute(self, name: str, *args, **kwargs):
        tool = self.get(name)

        if not tool:
            raise ValueError(f"Tool not found: {name}")

        return tool.func(*args, **kwargs)

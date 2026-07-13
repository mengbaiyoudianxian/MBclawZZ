from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Callable, Any


@dataclass
class RuntimeNode:

    name: str

    handler: Callable

    version: int = 1

    meta: Dict[str, Any] = field(default_factory=dict)


class RuntimeGraph:

    def __init__(self):

        self.nodes = {}

    def register(self, name: str, handler: Callable):

        self.nodes[name] = RuntimeNode(
            name=name,
            handler=handler
        )

    def execute(self, name: str, *args, **kwargs):

        node = self.nodes[name]

        return node.handler(*args, **kwargs)

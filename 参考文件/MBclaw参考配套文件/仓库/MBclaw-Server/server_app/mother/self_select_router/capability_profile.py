from dataclasses import dataclass


@dataclass
class AgentProfile:

    name: str

    strengths: list
    # coding / reasoning / vision / ui / search / fast_ops

    cost_level: float  # 0-1

    speed: float  # 0-1

    reliability: float  # 0-1

    tool_stack: list

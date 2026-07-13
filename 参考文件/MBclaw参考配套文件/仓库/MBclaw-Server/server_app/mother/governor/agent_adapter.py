# agent_adapter.py
# Agent Runtime Adapter Layer
# 作用：统一所有 Agent（Planner / Worker / Model / Evolution）调用接口

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class AgentContext:
    trace_id: str
    task_id: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class AgentResult:
    success: bool
    output: Any
    error: Optional[str]
    cost: float
    latency: float


class BaseAgent:
    """
    所有 Agent 必须继承该接口
    """

    name: str = "base_agent"

    async def run(self, context: AgentContext, payload: Dict[str, Any]) -> AgentResult:
        raise NotImplementedError


class FunctionAgent(BaseAgent):
    """
    将普通 async function 包装为 Agent
    """

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

    async def run(self, context: AgentContext, payload: Dict[str, Any]) -> AgentResult:
        start = time.time()
        try:
            result = await self.func(context, payload)
            return AgentResult(
                success=True,
                output=result,
                error=None,
                cost=0.0,
                latency=time.time() - start,
            )
        except Exception as e:
            return AgentResult(
                success=False,
                output=None,
                error=str(e),
                cost=0.0,
                latency=time.time() - start,
            )


class AgentRegistry:
    """
    Agent 注册中心（Kernel / Scheduler 使用）
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise ValueError(f"Agent not found: {name}")
        return self._agents[name]

    async def execute(self, name: str, context: AgentContext, payload: Dict[str, Any]):
        agent = self.get(name)
        return await agent.run(context, payload)

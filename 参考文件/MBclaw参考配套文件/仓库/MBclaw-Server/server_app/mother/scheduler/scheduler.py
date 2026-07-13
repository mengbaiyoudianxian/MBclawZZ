import time
import uuid
from scheduler.router import LLMRouter
from scheduler.types import ModelResponse


class Scheduler:

    def __init__(self, token_pool, cost_model, policy, eventbus=None):
        self.router = LLMRouter(token_pool, cost_model, policy)
        self.token_pool = token_pool
        self.cost_model = cost_model
        self.eventbus = eventbus

        self.model_backends = {
            "gpt-4o": self.fake_call,
            "gpt-4.1": self.fake_call,
            "claude": self.fake_call,
            "deepseek": self.fake_call,
            "local": self.fake_call
        }

    async def select(self, plan):
        task_type = plan.get("task_type", "chat")
        prompt = plan.get("prompt", "hello")

        request = type("Req", (), {
            "task_type": task_type,
            "prompt": prompt,
            "max_tokens": 2048,
            "budget": plan.get("budget", 1.0),
            "priority": plan.get("priority", 5),
        })()

        model = self.router.route(request)

        if self.eventbus:
            await self.eventbus.publish("model.selected", {
                "model": model,
                "task_type": task_type
            })

        return model

    async def execute_model(self, model, prompt, trace_id=None):
        start = time.time()

        try:
            output = await self.model_backends[model](prompt)
            latency = time.time() - start
            cost = self.cost_model.estimate(model, len(prompt) // 4)

            self.token_pool.record(
                provider=model, cost=cost, tokens=len(prompt) // 4,
                latency=latency, success=True
            )

            return ModelResponse(
                model=model, output=output, cost=cost, latency=latency,
                success=True, trace_id=trace_id
            )

        except Exception as e:
            self.token_pool.record(model, 0, 0, time.time() - start, False)
            return ModelResponse(
                model=model, output="", cost=0, latency=time.time() - start,
                success=False, error=str(e), trace_id=trace_id
            )

    async def fake_call(self, prompt):
        return f"[MODEL OUTPUT]: {prompt[:50]}"

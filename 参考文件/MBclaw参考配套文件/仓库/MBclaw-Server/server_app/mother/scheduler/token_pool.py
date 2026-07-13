import time
from collections import defaultdict


class TokenPool:

    def __init__(self):
        self.stats = defaultdict(lambda: {
            "cost": 0.0,
            "tokens": 0,
            "requests": 0,
            "failures": 0,
            "latency": []
        })

        self.quotas = {
            "openai": 100000,
            "deepseek": 100000,
            "claude": 80000,
            "local": 999999
        }

    def record(self, provider: str, cost: float, tokens: int, latency: float, success: bool):
        s = self.stats[provider]
        s["cost"] += cost
        s["tokens"] += tokens
        s["requests"] += 1
        s["latency"].append(latency)

        if not success:
            s["failures"] += 1

    def availability_score(self, provider: str):
        s = self.stats[provider]
        failure_rate = s["failures"] / max(1, s["requests"])
        avg_latency = sum(s["latency"][-20:]) / max(1, len(s["latency"][-20:]))
        quota_left = self.quotas.get(provider, 100000)
        return 1.0 / (1.0 + failure_rate + avg_latency * 0.1 + s["cost"] / 10 + (1 / (quota_left + 1)))

    def get_best_provider(self, candidates):
        return max(candidates, key=lambda p: self.availability_score(p))

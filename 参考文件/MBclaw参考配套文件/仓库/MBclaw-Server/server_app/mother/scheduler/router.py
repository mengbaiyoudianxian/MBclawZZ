import random


class LLMRouter:

    def __init__(self, token_pool, cost_model, policy):
        self.token_pool = token_pool
        self.cost_model = cost_model
        self.policy = policy

    def route(self, request):
        candidates = self.policy.select_candidates(request.task_type)
        scored = []

        for m in candidates:
            cost = self.cost_model.estimate(m, request.max_tokens)
            score = self.token_pool.availability_score(m)
            if cost > request.budget:
                score *= 0.2
            scored.append((m, score, cost))

        scored.sort(key=lambda x: x[1], reverse=True)

        if len(scored) > 1 and scored[0][1] == scored[1][1]:
            return random.choice(scored[:2])[0]

        return scored[0][0]

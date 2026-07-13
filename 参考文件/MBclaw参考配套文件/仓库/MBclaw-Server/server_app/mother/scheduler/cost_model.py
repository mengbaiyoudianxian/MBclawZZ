class CostModel:

    def __init__(self):
        self.price_table = {
            "gpt-4o": 0.01,
            "gpt-4.1": 0.02,
            "deepseek": 0.002,
            "claude": 0.015,
            "local": 0.0
        }

    def estimate(self, model: str, tokens: int):
        return self.price_table.get(model, 0.01) * tokens

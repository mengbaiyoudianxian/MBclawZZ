class AgentPool:

    def __init__(self):

        self.agents = {
            "claude": self._mock("claude"),
            "deepseek": self._mock("deepseek"),
            "mimo": self._mock("mimo"),
            "doubao": self._mock("doubao")
        }

    def _mock(self, name):

        def run(task):

            return f"[{name} executed]: {task}"

        return run

class TaskAnalyzer:

    def analyze(self, task: str):

        task_lower = task.lower()

        if "ui" in task_lower or "image" in task_lower:
            return "vision_ui"

        if "bug" in task_lower or "refactor" in task_lower:
            return "deep_coding"

        if "automation" in task_lower or "click" in task_lower:
            return "fast_ops"

        if "research" in task_lower or "design" in task_lower:
            return "reasoning"

        return "general"

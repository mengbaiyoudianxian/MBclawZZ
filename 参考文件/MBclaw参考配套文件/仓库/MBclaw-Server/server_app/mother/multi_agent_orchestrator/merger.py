class ResultMerger:

    def merge(self, task_results: dict):

        merged = "\n".join(str(v) for v in task_results.values())

        return {
            "final_output": merged,
            "components": task_results
        }

class ValidationPipeline:

    def validate(self, new_codebase):

        # prevent structural destruction
        required_modules = ["planner", "runtime", "memory"]

        for m in required_modules:

            if m not in new_codebase:
                return False

        return True

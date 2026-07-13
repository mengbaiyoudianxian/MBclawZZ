class SafetyGuard:

    def validate(self, mutation):

        # prevent dangerous core logic modification
        if "runtime_graph" in str(mutation.get("target")):
            return False

        if mutation.get("new_handler") is None:
            return False

        return True

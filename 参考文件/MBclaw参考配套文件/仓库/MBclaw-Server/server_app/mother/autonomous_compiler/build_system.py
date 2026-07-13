class BuildSystem:

    def build(self, codebase):

        runtime = {}

        for name, code in codebase.items():

            local_env = {}

            try:
                exec(code, {}, local_env)
                runtime[name] = local_env
            except Exception:
                pass

        return runtime

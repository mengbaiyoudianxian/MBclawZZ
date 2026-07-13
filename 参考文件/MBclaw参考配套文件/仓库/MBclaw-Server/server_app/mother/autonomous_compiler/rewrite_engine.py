class RewriteEngine:

    def generate_new_system(self, optimized_ir):

        new_codebase = {}

        for module_name in optimized_ir.modules:

            new_codebase[module_name] = f"""
# auto-generated module: {module_name}

class {module_name.capitalize()}:

    def run(self, *args, **kwargs):

        return "executed {module_name}"
"""

        return new_codebase

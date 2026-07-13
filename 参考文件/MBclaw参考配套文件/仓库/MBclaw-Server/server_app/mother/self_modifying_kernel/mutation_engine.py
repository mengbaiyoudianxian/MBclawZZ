class MutationEngine:

    def propose_mutation(self, node, new_handler):

        return {
            "target": node.name,
            "old_version": node.version,
            "new_handler": new_handler
        }

class PatchSystem:

    def apply_patch(self, runtime_graph, mutation):

        node = runtime_graph.nodes[mutation["target"]]

        node.handler = mutation["new_handler"]
        node.version += 1

        return {
            "status": "patched",
            "node": node.name,
            "new_version": node.version
        }

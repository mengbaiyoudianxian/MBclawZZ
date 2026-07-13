class HotReload:

    def reload_node(self, runtime_graph, name, new_handler):

        node = runtime_graph.nodes[name]

        node.handler = new_handler
        node.version += 1

        return f"{name} reloaded to v{node.version}"

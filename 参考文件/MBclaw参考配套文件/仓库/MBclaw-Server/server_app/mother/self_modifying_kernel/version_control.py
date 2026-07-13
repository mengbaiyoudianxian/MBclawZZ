class VersionControl:

    def __init__(self):

        self.snapshots = []

    def snapshot(self, runtime_graph):

        state = {
            name: node.version
            for name, node in runtime_graph.nodes.items()
        }

        self.snapshots.append(state)

    def rollback(self, runtime_graph, index=-1):

        snapshot = self.snapshots[index]

        for name, version in snapshot.items():

            if name in runtime_graph.nodes:
                runtime_graph.nodes[name].version = version

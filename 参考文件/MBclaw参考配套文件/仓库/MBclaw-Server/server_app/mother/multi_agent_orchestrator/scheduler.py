from collections import defaultdict


class Scheduler:

    def build_execution_order(self, tasks):

        graph = defaultdict(list)
        indegree = {}

        for t in tasks:

            indegree[t["id"]] = len(t["deps"])

            for d in t["deps"]:
                graph[d].append(t["id"])

        queue = [t["id"] for t in tasks if len(t["deps"]) == 0]

        order = []

        while queue:

            node = queue.pop(0)
            order.append(node)

            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        return order

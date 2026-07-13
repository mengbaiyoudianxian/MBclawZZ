from __future__ import annotations

from knowledge_graph.graph import KnowledgeGraph


class GraphReasoner:

    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph

    # -----------------------------
    # Bug -> Fix chain tracing
    # -----------------------------

    def trace_bug_root(self, node_id: str):

        visited = set()
        stack = [node_id]
        chain = []

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            node = self.graph.get(current)
            if not node:
                continue

            chain.append(node)

            edges = self.graph.neighbors(current)

            for e in edges:

                if e.relation in ["causes", "depends_on"]:
                    stack.append(e.target)

        return chain

    # -----------------------------
    # impact analysis (which modules does a fix affect)
    # -----------------------------

    def impact_analysis(self, node_id: str):

        return self.graph.neighbors(node_id)

from __future__ import annotations

from typing import List, Dict, Any


class TraceDashboard:
    """
    Prepares execution graph for visualization UI.
    """

    def build_graph(self, trace_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        nodes = []
        edges = []

        for i, e in enumerate(trace_events):
            nodes.append({
                "id": i,
                "label": e.get("event"),
            })

            if i > 0:
                edges.append({
                    "from": i - 1,
                    "to": i,
                })

        return {
            "nodes": nodes,
            "edges": edges,
        }

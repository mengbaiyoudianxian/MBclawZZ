from __future__ import annotations

from typing import Dict, List


class GraphMergeEngine:

    def merge(self, base_graph: Dict, incoming_graph: Dict):

        merged_nodes = {n["id"]: n for n in base_graph["nodes"]}

        # node merge
        for n in incoming_graph["nodes"]:

            if n["id"] in merged_nodes:

                # importance fusion
                merged_nodes[n["id"]]["importance"] = max(
                    merged_nodes[n["id"]].get("importance", 0.5),
                    n.get("importance", 0.5)
                )

            else:
                merged_nodes[n["id"]] = n

        # edge merge (dedup)
        merged_edges = set(
            tuple(e.items()) if isinstance(e, dict) else tuple(e)
            for e in base_graph["edges"]
        )

        for e in incoming_graph["edges"]:
            merged_edges.add(tuple(e.items()) if isinstance(e, dict) else tuple(e))

        return {
            "nodes": list(merged_nodes.values()),
            "edges": [dict(x) if isinstance(x, tuple) else x for x in merged_edges],
            "meta": {
                "merged": True
            }
        }

from __future__ import annotations

import uuid

from knowledge_graph_v2.entity import KGEntity
from engineering_brain.knowledge import EngineeringKnowledge


class KnowledgeUpdater:

    def __init__(self, graph, brain):

        self.graph = graph
        self.brain = brain

    # -----------------------------
    # write to graph + engineering brain
    # -----------------------------

    def update(self, structured_item: dict):

        node_id = str(uuid.uuid4())

        # -> Knowledge Graph
        self.graph.add_entity(
            KGEntity(
                id=node_id,
                type=structured_item["type"],
                name=structured_item["summary"][:30],
                content=structured_item["summary"],
                meta={
                    "tags": structured_item["tags"]
                },
                importance=structured_item["confidence"]
            )
        )

        # -> Engineering Brain (experience sediment)
        self.brain.add_knowledge(
            EngineeringKnowledge(
                id=node_id,
                type=structured_item["type"],
                title=structured_item["summary"][:50],
                content=structured_item["summary"],
                confidence=structured_item["confidence"],
                tags=structured_item["tags"]
            )
        )

from __future__ import annotations

from typing import List


class LearningQueue:

    def __init__(self):

        self.queue = []
        self.seen = set()

    # -----------------------------
    # dedup + enqueue
    # -----------------------------

    def push(self, item: dict):

        key = item["source"] + item["title"]

        if key in self.seen:
            return

        self.seen.add(key)

        self.queue.append(item)

    # -----------------------------
    # sort by importance
    # -----------------------------

    def sort(self):

        self.queue.sort(
            key=lambda x: len(x.get("content", "")),
            reverse=True
        )

    def pop_batch(self, n=5):

        batch = self.queue[:n]
        self.queue = self.queue[n:]
        return batch

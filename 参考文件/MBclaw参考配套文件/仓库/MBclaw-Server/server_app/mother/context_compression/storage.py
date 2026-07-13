from __future__ import annotations

from typing import List
from context_compression.models import Message, ContextBundle


class ContextStorage:

    def __init__(self):
        self.raw_log: List[Message] = []
        self.compressed_log: List[ContextBundle] = []

    # permanent raw record
    def append_raw(self, msg: Message):
        self.raw_log.append(msg)

    # store compressed version
    def store_compressed(self, bundle: ContextBundle):
        self.compressed_log.append(bundle)

    def get_raw(self):
        return self.raw_log

    def get_latest(self):
        return self.compressed_log[-1] if self.compressed_log else None

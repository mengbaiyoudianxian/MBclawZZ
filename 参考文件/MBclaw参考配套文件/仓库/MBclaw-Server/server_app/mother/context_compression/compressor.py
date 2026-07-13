from __future__ import annotations

from context_compression.storage import ContextStorage
from context_compression.policy import CompressionPolicy
from context_compression.models import ContextBundle, Message, WorkspaceState
from context_compression.detector import ContextWindowDetector


class ContextCompressionEngine:

    def __init__(self):
        self.storage = ContextStorage()
        self.policy = CompressionPolicy()
        self.detector = ContextWindowDetector()

    # -------------------------
    # ingest raw message
    # -------------------------

    def ingest(self, msg: Message):
        self.storage.append_raw(msg)

    # -------------------------
    # compress
    # -------------------------

    def compress(self, model_name: str, used_tokens: int, workspace: WorkspaceState):

        window = self.detector.detect_window(model_name)

        if not self.detector.should_compress(used_tokens, window):
            return None  # no compression needed

        bundle = ContextBundle(
            raw_messages=self.storage.get_raw(),
            workspace=workspace
        )

        compressed = self.policy.apply(bundle)

        self.storage.store_compressed(bundle)

        return compressed

    # -------------------------
    # build LLM context
    # -------------------------

    def build_context(self, model_name: str, used_tokens: int, workspace: WorkspaceState):

        compressed = self.compress(model_name, used_tokens, workspace)

        if compressed:
            return compressed

        # fallback full context
        return {
            "raw": [m.__dict__ for m in self.storage.get_raw()],
            "workspace": workspace.__dict__
        }

from __future__ import annotations

from context_compression.models import ContextBundle, Message, WorkspaceState


class CompressionPolicy:

    def compress_dialogue(self, messages: list[Message]) -> list[str]:
        """
        Keep decision-level summaries only
        """
        summary = []

        for m in messages:
            if m.role == "assistant":
                summary.append("DECISION: " + m.content[:200])
            elif m.role == "user":
                summary.append("REQUEST: " + m.content[:200])

        return summary

    def compress_workspace(self, ws: WorkspaceState):

        return {
            "todo": ws.todo[-20:],  # keep latest tasks
            "code_diff": ws.code_diff[-10:],  # last diffs only
            "key_artifacts": ws.key_artifacts,
        }

    def apply(self, bundle: ContextBundle):

        return {
            "dialogue_summary": self.compress_dialogue(bundle.raw_messages),
            "workspace": self.compress_workspace(bundle.workspace),
            "memory_refs": bundle.memory_refs,
        }

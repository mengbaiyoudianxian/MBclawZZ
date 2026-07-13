from __future__ import annotations

from gateway.message import UnifiedMessage


class MessageNormalizer:

    def normalize(self, raw: dict, source: str) -> UnifiedMessage:

        """
        Normalize QQ / WeChat / Feishu / Web messages into unified structure
        """

        return UnifiedMessage(
            source=source,
            user_id=self._map_user(raw),
            session_id=self._map_session(raw),
            type=self._detect_type(raw),
            content=self._extract_content(raw),
            meta=raw.get("meta", {})
        )

    def _map_user(self, raw): return raw.get("user_id", "unknown")

    def _map_session(self, raw): return raw.get("session_id", "default")

    def _detect_type(self, raw):

        if "image" in raw:
            return "image"
        if "cmd" in raw:
            return "command"
        return "text"

    def _extract_content(self, raw):
        return raw.get("content", "")

from __future__ import annotations


class ContextWindowDetector:

    def __init__(self):
        # default heuristic windows
        self.model_windows = {
            "small": 8000,
            "medium": 32000,
            "large": 128000,
        }

    def detect_window(self, model_name: str) -> int:
        for k, v in self.model_windows.items():
            if k in model_name.lower():
                return v
        return 32000  # fallback

    def should_compress(self, used_tokens: int, model_window: int) -> bool:
        ratio = used_tokens / model_window
        return ratio >= 0.85  # 80-90% trigger zone

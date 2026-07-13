from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    max_iterations: int = int(os.getenv("MOTHER_MAX_ITERATIONS", "50"))
    default_budget: float = float(os.getenv("MOTHER_DEFAULT_BUDGET", "5.0"))
    concurrency: int = int(os.getenv("MOTHER_CONCURRENCY", "4"))
    max_replans: int = int(os.getenv("MOTHER_MAX_REPLANS", "2"))
    runtime_db: str = os.getenv("MOTHER_RUNTIME_DB", "/var/lib/mbclaw/mother_runtime.db")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    aliyun_dash_scope_key: str = os.getenv("ALIYUN_DASH_SCOPE_KEY", "")
    zhipu_key: str = os.getenv("ZHIPU_KEY", "")


config = Config()

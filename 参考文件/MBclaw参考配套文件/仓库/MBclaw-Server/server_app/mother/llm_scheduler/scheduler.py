from __future__ import annotations

from typing import List

from llm_router.provider import Provider
from llm_router.models import LLMRequest, LLMResponse
from llm_scheduler.token_pool import TokenPool
from llm_scheduler.router import Router


class LLMModelScheduler:

    def __init__(self, providers: List[Provider], pool: TokenPool):
        self.router = Router(providers, pool)

    def schedule(self, req: LLMRequest) -> LLMResponse:
        return self.router.route(req)

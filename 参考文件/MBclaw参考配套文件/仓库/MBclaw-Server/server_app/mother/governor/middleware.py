from __future__ import annotations

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .governor import Governor
from .models import Proposal, Action, ContextState
from .enums import ActionType


class GovernorMiddleware(BaseHTTPMiddleware):
    """
    Intercepts HTTP requests and routes them through Governor.
    """

    def __init__(self, app, governor: Governor):
        super().__init__(app)
        self.governor = governor

    async def dispatch(self, request: Request, call_next):
        body = await request.body()

        # minimal interpretation layer
        action = Action(
            type=ActionType.SYSTEM,
            name=f"{request.method}:{request.url.path}",
            payload={"body": body.decode("utf-8", errors="ignore")},
        )

        proposal = Proposal(
            actions=[action],
            context=ContextState(),
            rationale="http_request",
        )

        decision = self.governor.evaluate(proposal)

        if decision.status.value != "approved":
            return Response(
                content="Blocked by Governor",
                status_code=403,
            )

        return await call_next(request)

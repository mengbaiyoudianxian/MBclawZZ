from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from .enums import ActionType, DecisionStatus, RiskLevel, AuditLevel, RollbackReason


def _id():
    return str(uuid4())


class ContextState(BaseModel):
    context_id: str = Field(default_factory=_id)
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    variables: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Action(BaseModel):
    action_id: str = Field(default_factory=_id)

    type: ActionType
    name: str
    payload: Dict[str, Any] = Field(default_factory=dict)

    target: Optional[str] = None
    source: Optional[str] = None

    risk_hint: RiskLevel = RiskLevel.LOW

    created_at: datetime = Field(default_factory=datetime.utcnow)


class Proposal(BaseModel):
    proposal_id: str = Field(default_factory=_id)

    actions: List[Action]

    context: ContextState

    rationale: Optional[str] = None

    estimated_risk: RiskLevel = RiskLevel.NONE

    tags: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class Decision(BaseModel):
    decision_id: str = Field(default_factory=_id)

    proposal_id: str

    status: DecisionStatus

    final_risk: RiskLevel

    reason: Optional[str] = None

    policy_trace: List[str] = Field(default_factory=list)
    risk_trace: List[str] = Field(default_factory=list)

    approved_actions: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditRecord(BaseModel):
    audit_id: str = Field(default_factory=_id)

    level: AuditLevel

    event: str

    actor: Optional[str] = None

    target: Optional[str] = None

    data: Dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RollbackRecord(BaseModel):
    rollback_id: str = Field(default_factory=_id)

    reason: RollbackReason

    related_decision_id: Optional[str] = None

    state_snapshot: Dict[str, Any] = Field(default_factory=dict)

    success: bool = False

    timestamp: datetime = Field(default_factory=datetime.utcnow)

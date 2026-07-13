from enum import Enum, IntEnum


class ActionType(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    NETWORK = "network"
    TOOL_CALL = "tool_call"
    SYSTEM = "system"


class DecisionStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"
    REVIEW = "review"
    OVERRIDDEN = "overridden"


class RiskLevel(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class PolicyLevel(IntEnum):
    PERMISSIVE = 0
    STANDARD = 1
    STRICT = 2
    LOCKDOWN = 3


class AuditLevel(str, Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"


class RollbackReason(str, Enum):
    POLICY_FAIL = "policy_fail"
    RISK_FAIL = "risk_fail"
    EXECUTION_ERROR = "execution_error"
    MANUAL = "manual"

class GovernorException(Exception):
    """Base exception for Governor system."""


class PolicyViolation(GovernorException):
    def __init__(self, message: str, policy_id: str | None = None):
        self.policy_id = policy_id
        super().__init__(message)


class RiskViolation(GovernorException):
    def __init__(self, message: str, risk_level: int | None = None):
        self.risk_level = risk_level
        super().__init__(message)


class ExecutionBlocked(GovernorException):
    def __init__(self, message: str, action_id: str | None = None):
        self.action_id = action_id
        super().__init__(message)


class ValidationError(GovernorException):
    pass


class UnauthorizedAction(GovernorException):
    pass


class GovernorInternalError(GovernorException):
    pass

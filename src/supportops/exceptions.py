class SupportOpsError(Exception):
    """Base class for all application errors."""


class InvalidMessageError(SupportOpsError):
    """Raised when a customer message is empty or invalid."""
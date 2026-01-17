"""Custom exception classes for the Dermalytics SDK."""


class DermalyticsError(Exception):
    """Base exception for all Dermalytics SDK errors."""

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(self.message)


class APIError(DermalyticsError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class AuthenticationError(DermalyticsError):
    """Raised when authentication fails."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class NotFoundError(DermalyticsError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class RateLimitError(DermalyticsError):
    """Raised when the rate limit is exceeded."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class ValidationError(DermalyticsError):
    """Raised when request validation fails."""

    def __init__(self, message: str = ""):
        super().__init__(message)

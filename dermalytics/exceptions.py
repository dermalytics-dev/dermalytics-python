"""Custom exception classes for the Dermalytics SDK."""


class DermalyticsError(Exception):
    """Base exception for all Dermalytics SDK errors."""
    pass


class APIError(DermalyticsError):
    """Raised when the API returns an error response."""
    pass


class AuthenticationError(DermalyticsError):
    """Raised when authentication fails."""
    pass


class NotFoundError(DermalyticsError):
    """Raised when a requested resource is not found."""
    pass


class RateLimitError(DermalyticsError):
    """Raised when the rate limit is exceeded."""
    pass


class ValidationError(DermalyticsError):
    """Raised when request validation fails."""
    pass

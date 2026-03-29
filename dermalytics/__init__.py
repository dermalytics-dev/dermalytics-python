"""Dermalytics SDK for Python - Skincare Ingredient Analysis API."""

from .client import Dermalytics
from .exceptions import (
    DermalyticsError,
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__version__ = "0.1.4"
__all__ = [
    "Dermalytics",
    "DermalyticsError",
    "APIError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]

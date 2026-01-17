"""Dermalytics SDK for Python - Skincare Ingredient Analysis API."""

from .client import Dermalytics
from .exceptions import (
    DermalyticsError,
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "Dermalytics",
    "DermalyticsError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]

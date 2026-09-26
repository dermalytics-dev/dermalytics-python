"""Dermalytics SDK for Python - Skincare Ingredient Analysis API."""

from .client import Dermalytics
from .types import IngredientSearchResponse, ProductSearchResponse, ProductResponse
from .exceptions import (
    DermalyticsError,
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__version__ = "1.0.0"
__all__ = [
    "Dermalytics",
    "IngredientSearchResponse",
    "ProductSearchResponse",
    "ProductResponse",
    "DermalyticsError",
    "APIError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]

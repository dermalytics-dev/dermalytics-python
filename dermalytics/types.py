"""Type definitions for the Dermalytics SDK."""

from typing import TypedDict, List, Optional


class Category(TypedDict):
    """Ingredient category information."""
    name: str
    slug: str


class ConditionSafety(TypedDict):
    """Safety information for a specific condition."""
    condition: str
    severity: str
    reason: str


class Ingredient(TypedDict):
    """Ingredient information."""
    name: str
    severity: str
    description: Optional[str]
    category: Category
    condition_safeties: List[ConditionSafety]
    synonyms: List[str]


class IngredientAnalysis(TypedDict):
    """Ingredient analysis result."""
    name: str
    severity: str
    category: str


class Warning(TypedDict):
    """Product analysis warning."""
    ingredient: str
    condition: str
    severity: str
    reason: str


class ProductAnalysis(TypedDict):
    """Product analysis result."""
    safety_status: str
    ingredients: List[IngredientAnalysis]
    warnings: List[Warning]

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
    comedogenicity: Optional[int]
    irritancy: Optional[int]
    formula: Optional[str]
    molecular_weight: Optional[float]
    cas_no: Optional[str]
    ec_no: Optional[str]
    ph_eur_name: Optional[str]
    functions: List[str]
    categories: List[Category]
    condition_safeties: List[ConditionSafety]
    synonyms: List[str]
    credits_remaining: int


class IngredientAnalysis(TypedDict):
    """Ingredient analysis result."""
    name: str
    found: bool
    severity: str
    category: Optional[str]
    description: Optional[str]
    comedogenicity: Optional[int]
    irritancy: Optional[int]
    formula: Optional[str]
    molecular_weight: Optional[float]
    cas_no: Optional[str]
    ec_no: Optional[str]
    ph_eur_name: Optional[str]
    functions: List[str]


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
    credits_remaining: int

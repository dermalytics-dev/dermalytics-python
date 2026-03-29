"""Type definitions for the Dermalytics SDK."""

from typing import TypedDict, List, Optional


class Ingredient(TypedDict):
    """Single-ingredient lookup response (GET /v1/ingredients/{name})."""

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
    category: Optional[str]
    synonyms: List[str]
    credits_remaining: int


class IngredientAnalysis(TypedDict):
    """One row from POST /v1/analyze."""

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


class ProductAnalysis(TypedDict):
    """Batch analysis response (POST /v1/analyze)."""

    safety_status: str
    ingredients: List[IngredientAnalysis]
    credits_remaining: int

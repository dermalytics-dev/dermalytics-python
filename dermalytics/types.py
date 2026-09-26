"""Type definitions for the Dermalytics SDK."""

from typing import TypedDict, List, Literal, Optional


TraitFlag = Literal[
    "drying_alcohol",
    "fragrance",
    "paraben",
    "silicone",
    "sulfate",
    "oil",
    "fungal_acne_trigger",
    "reef_unsafe",
    "eu_allergen",
]


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
    trait_flags: List[TraitFlag]
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
    trait_flags: List[TraitFlag]


class ProductAnalysis(TypedDict):
    """Batch analysis response (POST /v1/analyze)."""

    safety_status: str
    ingredients: List[IngredientAnalysis]
    credits_remaining: int


class SearchPagination(TypedDict):
    limit: int
    offset: int
    next_offset: Optional[int]


class RatingsAvailable(TypedDict):
    comedogenicity: bool
    irritancy: bool


class IngredientSearchItem(TypedDict):
    id: str
    name: str
    cas_no: Optional[str]
    ec_no: Optional[str]
    functions: List[str]
    ratings_available: RatingsAvailable
    record_updated_at: str


class ProductSummary(TypedDict):
    id: str
    name: str
    brand: Optional[str]
    category: Optional[str]
    ingredients_count: int
    area: Optional[Literal["face", "eyes", "lips", "body", "hair", "nails"]]
    # Stored derived tags, not independently verified product claims.
    traits_cache: List[str]
    key_ingredient_tags: List[str]


class ProductIngredientItem(TypedDict):
    id: str
    name: str
    position: Optional[int]


class IngredientSearchResponse(TypedDict):
    data: List[IngredientSearchItem]
    pagination: SearchPagination
    credits_remaining: int


class ProductSearchResponse(TypedDict):
    data: List[ProductSummary]
    pagination: SearchPagination
    credits_remaining: int


class ProductResponse(ProductSummary):
    ingredients: List[ProductIngredientItem]
    credits_remaining: int

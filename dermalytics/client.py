"""Main API client for the Dermalytics SDK."""

from typing import List, Optional
from .exceptions import DermalyticsError
from .types import Ingredient, ProductAnalysis


class Dermalytics:
    """Client for interacting with the Dermalytics API.
    
    This SDK is currently a placeholder. Full implementation coming soon.
    
    Args:
        api_key: Your Dermalytics API key
        base_url: Optional base URL for the API (defaults to https://api.dermalytics.dev)
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.dermalytics.dev"
    
    def get_ingredient(self, name: str) -> Ingredient:
        """Get detailed information about a specific ingredient.
        
        Args:
            name: The name of the ingredient to look up
            
        Returns:
            Ingredient information including safety ratings, category, and condition safeties
            
        Raises:
            NotImplementedError: This SDK is currently a placeholder
        """
        raise NotImplementedError(
            "This SDK is a placeholder. Full implementation coming soon."
        )
    
    def analyze_product(self, ingredients: List[str]) -> ProductAnalysis:
        """Analyze a complete product formulation.
        
        Args:
            ingredients: List of ingredient names in the product
            
        Returns:
            Product analysis including safety status, ingredient details, and warnings
            
        Raises:
            NotImplementedError: This SDK is currently a placeholder
        """
        raise NotImplementedError(
            "This SDK is a placeholder. Full implementation coming soon."
        )

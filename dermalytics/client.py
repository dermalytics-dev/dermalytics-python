"""Main API client for the Dermalytics SDK."""

import json
import re
from typing import List, Optional, Dict, Any, cast
from urllib.parse import quote, urlencode

import requests

from ._public_response import public_response

from .exceptions import (
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from .types import Ingredient, ProductAnalysis, IngredientSearchResponse, ProductSearchResponse, ProductResponse


class Dermalytics:
    """Client for interacting with the Dermalytics API.
    
    Args:
        api_key: Optional Dermalytics API key; omit for five free requests per IP per 24 hours
        base_url: Optional base URL for the API (defaults to https://api.dermalytics.dev)
        
    Raises:
        ValidationError: If a provided API key is empty or invalid
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        if api_key is not None and (not isinstance(api_key, str) or not api_key.strip()):
            raise ValidationError("API key is required")
        
        self.api_key = api_key.strip() if api_key is not None else None
        self.signup_url: Optional[str] = None
        self.base_url = (base_url or "https://api.dermalytics.dev").rstrip("/")
    
    def _request(
        self, endpoint: str, kind: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API with proper error handling.
        
        Args:
            endpoint: API endpoint path (e.g., "/v1/ingredients/niacinamide")
            method: HTTP method (default: "GET")
            data: Optional data to send in request body (for POST requests)
            
        Returns:
            JSON response as dictionary
            
        Raises:
            APIError: For network errors or invalid responses
            AuthenticationError: For 401/403 responses
            NotFoundError: For 404 responses
            RateLimitError: For 429 responses
            ValidationError: For 400 responses
        """
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(
                    url, headers=headers, json=data, timeout=30
                )
            else:
                raise APIError(f"Unsupported HTTP method: {method}")
        except requests.exceptions.RequestException as e:
            # Network errors (connection failed, timeout, etc.)
            raise APIError(
                str(e) if isinstance(e, Exception) else "Network request failed"
            )
        
        signup = response.headers.get("X-API-Key-URL")
        self.signup_url = signup if isinstance(signup, str) and signup.startswith("https://") else None

        if not response.ok:
            self._handle_error_response(response)
        
        try:
            return public_response(response.json(), kind)
        except (ValueError, json.JSONDecodeError):
            # JSON parsing errors
            raise APIError("Invalid response format from server")
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses from the API based on HTTP status codes.
        
        Args:
            response: The requests.Response object with error status
            
        Raises:
            AuthenticationError: For 401/403 responses
            NotFoundError: For 404 responses
            RateLimitError: For 429 responses
            ValidationError: For 400 responses
            APIError: For other error responses
        """
        error_message = f"HTTP {response.status_code}: {response.reason}"
        
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                error_obj = error_data.get("error")
                if isinstance(error_obj, dict):
                    error_message = error_obj.get("message") or error_message
                else:
                    error_message = error_data.get("message") or error_message
        except (ValueError, json.JSONDecodeError):
            pass

        status_code = response.status_code
        if status_code in (401, 403):
            raise AuthenticationError(error_message)
        elif status_code == 402:
            raise InsufficientCreditsError(error_message)
        elif status_code == 404:
            raise NotFoundError(error_message)
        elif status_code == 429:
            raise RateLimitError(error_message)
        elif status_code == 400:
            raise ValidationError(error_message)
        elif status_code in (500, 502, 503, 504):
            raise APIError(f"Server error: {error_message}")
        else:
            raise APIError(error_message)
    
    def get_ingredient(self, name: str) -> Ingredient:
        """Get detailed information about a specific ingredient.
        
        Args:
            name: The name of the ingredient to look up
            
        Returns:
            Ingredient information including safety rating and category
            
        Raises:
            ValidationError: If the ingredient name is invalid
            NotFoundError: If the ingredient is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
        """
        if not name or not isinstance(name, str) or not name.strip():
            raise ValidationError("Ingredient name is required")
        
        encoded_name = quote(name.strip(), safe="")
        return self._request(f"/v1/ingredients/{encoded_name}", "ingredient")  # type: ignore
    
    def analyze_product(self, ingredients: List[str]) -> ProductAnalysis:
        """Analyze a complete product formulation.
        
        Args:
            ingredients: List of ingredient names in the product
            
        Returns:
            Product analysis including safety status and per-ingredient results
            
        Raises:
            ValidationError: If the ingredients array is invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
        """
        if not isinstance(ingredients, list) or len(ingredients) == 0:
            raise ValidationError(
                "Ingredients array is required and must not be empty"
            )
        
        if not self.api_key and (len(ingredients) > 5 or any(
            not isinstance(value, str) or not value.strip() or len(value) > 100 for value in ingredients
        )):
            raise ValidationError("Without an API key, provide 1–5 ingredient names of 1–100 characters each")

        return self._request(
            "/v1/analyze", "analysis", method="POST", data={"ingredients": ingredients}
        )  # type: ignore

    def _search_limit(self, limit: Optional[int], offset: int) -> int:
        resolved = (20 if self.api_key else 3) if limit is None else limit
        if not self.api_key and (type(resolved) is not int or resolved > 3 or offset != 0):
            raise ValidationError("Without an API key, use limit 1–3 and offset 0")
        return resolved

    @staticmethod
    def _search_params(query: str, limit: int, offset: int) -> Dict[str, str]:
        if not isinstance(query, str) or not 2 <= len(query.strip()) <= 100:
            raise ValidationError("Search query must contain 2–100 characters")
        if type(limit) is not int or not 1 <= limit <= 50:
            raise ValidationError("limit must be an integer from 1 to 50")
        if type(offset) is not int or not 0 <= offset <= 10000:
            raise ValidationError("offset must be an integer from 0 to 10000")
        return {"q": query.strip(), "limit": str(limit), "offset": str(offset)}

    def search_ingredients(
        self, query: str, *, limit: Optional[int] = None, offset: int = 0
    ) -> IngredientSearchResponse:
        """Search names, synonyms or exact CAS/EC identifiers; one credit per non-empty page."""
        params = urlencode(self._search_params(query, self._search_limit(limit, offset), offset))
        return cast(IngredientSearchResponse, self._request(f"/v1/ingredients?{params}", "ingredientSearch"))

    def search_products(
        self, query: str, *, limit: Optional[int] = None, offset: int = 0,
        brand: Optional[str] = None, ingredient: Optional[str] = None
    ) -> ProductSearchResponse:
        """Search the available catalog. Product availability depends on the deployment."""
        params = self._search_params(query, self._search_limit(limit, offset), offset)
        for name, value in (("brand", brand), ("ingredient", ingredient)):
            if value is not None:
                if not isinstance(value, str) or not 1 <= len(value.strip()) <= 255:
                    raise ValidationError(f"{name} must contain 1–255 characters")
                params[name] = value.strip()
        return cast(ProductSearchResponse, self._request(f"/v1/products?{urlencode(params)}", "productSearch"))

    def get_product(self, product_id: str) -> ProductResponse:
        """Get a product and stored ingredient list by UUID; one credit on success."""
        if not isinstance(product_id, str) or not re.fullmatch(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
            product_id, re.IGNORECASE
        ):
            raise ValidationError("Product id must be a UUID")
        return cast(ProductResponse, self._request(f"/v1/products/{quote(product_id, safe='')}", "product"))

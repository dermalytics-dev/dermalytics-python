"""Main API client for the Dermalytics SDK."""

import json
from typing import List, Optional, Dict, Any
from urllib.parse import quote

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from .types import Ingredient, ProductAnalysis


class Dermalytics:
    """Client for interacting with the Dermalytics API.
    
    Args:
        api_key: Your Dermalytics API key
        base_url: Optional base URL for the API (defaults to https://api.dermalytics.dev)
        
    Raises:
        ValidationError: If API key is missing or invalid
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            raise ValidationError("API key is required")
        
        self.api_key = api_key.strip()
        self.base_url = (base_url or "https://api.dermalytics.dev").rstrip("/")
    
    def _request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API with proper error handling.
        
        Args:
            endpoint: API endpoint path (e.g., "/ingredients/niacinamide")
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
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
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
        
        if not response.ok:
            self._handle_error_response(response)
        
        try:
            return response.json()
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
                error_message = (
                    error_data.get("message")
                    or error_data.get("error")
                    or error_message
                )
        except (ValueError, json.JSONDecodeError):
            # If JSON parsing fails, use the status text
            pass
        
        status_code = response.status_code
        if status_code in (401, 403):
            raise AuthenticationError(error_message)
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
            Ingredient information including safety ratings, category, and condition safeties
            
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
        return self._request(f"/ingredients/{encoded_name}")  # type: ignore
    
    def analyze_product(self, ingredients: List[str]) -> ProductAnalysis:
        """Analyze a complete product formulation.
        
        Args:
            ingredients: List of ingredient names in the product
            
        Returns:
            Product analysis including safety status, ingredient details, and warnings
            
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
        
        return self._request(
            "/analyze", method="POST", data={"ingredients": ingredients}
        )  # type: ignore

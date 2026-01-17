"""Tests for the Dermalytics client."""

from unittest.mock import Mock, patch
import pytest
import requests

from dermalytics import Dermalytics
from dermalytics.exceptions import (
    ValidationError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    APIError,
)


def test_client_initialization():
    """Test that client can be initialized."""
    client = Dermalytics(api_key="test_key")
    assert client is not None
    assert client.api_key == "test_key"
    assert client.base_url == "https://api.dermalytics.dev"


def test_client_initialization_with_base_url():
    """Test that client can be initialized with custom base URL."""
    client = Dermalytics(api_key="test_key", base_url="https://custom.api.dev")
    assert client.base_url == "https://custom.api.dev"


def test_client_initialization_with_trailing_slash():
    """Test that trailing slash is removed from base URL."""
    client = Dermalytics(api_key="test_key", base_url="https://api.dermalytics.dev/")
    assert client.base_url == "https://api.dermalytics.dev"


def test_client_initialization_with_empty_api_key():
    """Test that empty API key raises ValidationError."""
    with pytest.raises(ValidationError, match="API key is required"):
        Dermalytics(api_key="")


def test_client_initialization_with_whitespace_api_key():
    """Test that whitespace-only API key raises ValidationError."""
    with pytest.raises(ValidationError, match="API key is required"):
        Dermalytics(api_key="   ")


def test_client_initialization_trims_api_key():
    """Test that API key is trimmed."""
    client = Dermalytics(api_key="  test_key  ")
    assert client.api_key == "test_key"


@patch("dermalytics.client.requests.get")
def test_get_ingredient_success(mock_get):
    """Test successful get_ingredient call."""
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "name": "niacinamide",
        "severity": "safe",
        "description": "A form of vitamin B3",
        "category": {"name": "Vitamins", "slug": "vitamins"},
        "condition_safeties": [],
        "synonyms": ["nicotinamide"],
    }
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    ingredient = client.get_ingredient("niacinamide")
    
    assert ingredient["name"] == "niacinamide"
    assert ingredient["severity"] == "safe"
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert "Bearer test_key" in call_args[1]["headers"]["Authorization"]


@patch("dermalytics.client.requests.get")
def test_get_ingredient_with_encoding(mock_get):
    """Test that ingredient name is URL encoded."""
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "name": "salicylic acid",
        "severity": "low_risk",
        "category": {"name": "Acids", "slug": "acids"},
        "condition_safeties": [],
        "synonyms": [],
    }
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    client.get_ingredient("salicylic acid")
    
    call_args = mock_get.call_args
    assert "/ingredients/salicylic%20acid" in call_args[0][0]


def test_get_ingredient_validation_empty_name():
    """Test that empty ingredient name raises ValidationError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(ValidationError, match="Ingredient name is required"):
        client.get_ingredient("")


def test_get_ingredient_validation_whitespace_name():
    """Test that whitespace-only ingredient name raises ValidationError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(ValidationError, match="Ingredient name is required"):
        client.get_ingredient("   ")


@patch("dermalytics.client.requests.get")
def test_get_ingredient_not_found(mock_get):
    """Test that 404 response raises NotFoundError."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.json.return_value = {"message": "Ingredient not found"}
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(NotFoundError, match="Ingredient not found"):
        client.get_ingredient("nonexistent")


@patch("dermalytics.client.requests.get")
def test_get_ingredient_authentication_error(mock_get):
    """Test that 401 response raises AuthenticationError."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_response.reason = "Unauthorized"
    mock_response.json.return_value = {"message": "Invalid API key"}
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(AuthenticationError, match="Invalid API key"):
        client.get_ingredient("niacinamide")


@patch("dermalytics.client.requests.get")
def test_get_ingredient_rate_limit_error(mock_get):
    """Test that 429 response raises RateLimitError."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 429
    mock_response.reason = "Too Many Requests"
    mock_response.json.return_value = {"message": "Rate limit exceeded"}
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        client.get_ingredient("niacinamide")


@patch("dermalytics.client.requests.post")
def test_analyze_product_success(mock_post):
    """Test successful analyze_product call."""
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "safety_status": "safe",
        "ingredients": [
            {"name": "Aqua", "severity": "safe", "category": "Water"}
        ],
        "warnings": [],
    }
    mock_post.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    analysis = client.analyze_product(["Aqua", "Glycerin"])
    
    assert analysis["safety_status"] == "safe"
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args[1]["json"] == {"ingredients": ["Aqua", "Glycerin"]}


def test_analyze_product_validation_empty_list():
    """Test that empty ingredients list raises ValidationError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(
        ValidationError, match="Ingredients array is required and must not be empty"
    ):
        client.analyze_product([])


def test_analyze_product_validation_not_list():
    """Test that non-list ingredients raises ValidationError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(
        ValidationError, match="Ingredients array is required and must not be empty"
    ):
        client.analyze_product("not a list")  # type: ignore


@patch("dermalytics.client.requests.post")
def test_analyze_product_validation_error(mock_post):
    """Test that 400 response raises ValidationError."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.reason = "Bad Request"
    mock_response.json.return_value = {"message": "Invalid ingredients"}
    mock_post.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(ValidationError, match="Invalid ingredients"):
        client.analyze_product(["invalid"])


@patch("dermalytics.client.requests.get")
def test_network_error(mock_get):
    """Test that network errors raise APIError."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(APIError):
        client.get_ingredient("niacinamide")


@patch("dermalytics.client.requests.get")
def test_invalid_json_response(mock_get):
    """Test that invalid JSON response raises APIError."""
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(APIError, match="Invalid response format from server"):
        client.get_ingredient("niacinamide")


@patch("dermalytics.client.requests.get")
def test_server_error(mock_get):
    """Test that 500 response raises APIError with server error prefix."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.reason = "Internal Server Error"
    mock_response.json.return_value = {"message": "Internal error"}
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    with pytest.raises(APIError, match="Server error"):
        client.get_ingredient("niacinamide")

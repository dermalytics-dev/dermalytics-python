"""Tests for the Dermalytics client."""

from unittest.mock import Mock, patch
import pytest
import requests
from urllib.parse import urlparse, parse_qs

from dermalytics import Dermalytics
from dermalytics.exceptions import (
    ValidationError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    APIError,
)


@patch("dermalytics.client.requests.get")
def test_search_products_encodes_filters_and_preserves_pagination(mock_get):
    result = {"data": [{"name": "A&B", "brand": None}], "pagination": {"limit": 2, "offset": 0, "next_offset": 2}, "credits_remaining": 99}
    mock_get.return_value = Mock(ok=True, json=Mock(return_value=result))
    client = Dermalytics("fixture")
    assert client.search_products(" A&B ", limit=2, brand="Example / Co", ingredient="Vitamin B3") == result
    url = urlparse(mock_get.call_args[0][0])
    assert url.path == "/v1/products"
    assert parse_qs(url.query) == {"q": ["A&B"], "limit": ["2"], "offset": ["0"], "brand": ["Example / Co"], "ingredient": ["Vitamin B3"]}


@patch("dermalytics.client.requests.get")
def test_search_ingredients_empty_page(mock_get):
    result = {"data": [], "pagination": {"limit": 20, "offset": 0, "next_offset": None}, "credits_remaining": 100}
    mock_get.return_value = Mock(ok=True, json=Mock(return_value=result))
    assert Dermalytics("fixture").search_ingredients("98-92-0") == result
    assert "/v1/ingredients?q=98-92-0&" in mock_get.call_args[0][0]


@patch("dermalytics.client.requests.get")
def test_catalog_validation_happens_before_request(mock_get):
    client = Dermalytics("fixture")
    for options in [{"limit": 51}, {"limit": True}, {"offset": -1}, {"offset": 1.5}, {"brand": " "}]:
        with pytest.raises(ValidationError):
            client.search_products("cream", **options)
    with pytest.raises(ValidationError):
        client.search_ingredients("x")
    with pytest.raises(ValidationError):
        client.get_product("../private")
    mock_get.assert_not_called()


@patch("dermalytics.client.requests.get")
def test_product_detail_and_unavailable_catalog(mock_get):
    result = {"id": "f879d134-c8e3-4816-a7ad-a042508c44e5", "ingredients": [], "credits_remaining": 99}
    mock_get.return_value = Mock(ok=True, json=Mock(return_value=result))
    client = Dermalytics("fixture")
    assert client.get_product(result["id"]) == result
    assert mock_get.call_args[0][0].endswith("/v1/products/" + result["id"])
    mock_get.return_value = Mock(ok=False, status_code=503, reason="Unavailable", json=Mock(return_value={"error": {"code": "CATALOG_UNAVAILABLE", "message": "Catalog not enabled"}}))
    with pytest.raises(APIError, match="Catalog not enabled"):
        client.search_products("cream")


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
        "comedogenicity": None,
        "irritancy": None,
        "formula": None,
        "molecular_weight": None,
        "cas_no": None,
        "ec_no": None,
        "ph_eur_name": None,
        "functions": [],
        "trait_flags": [],
        "category": "Vitamins",
        "synonyms": ["nicotinamide"],
        "credits_remaining": 99,
    }
    mock_get.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    ingredient = client.get_ingredient("niacinamide")
    
    assert ingredient["name"] == "niacinamide"
    assert ingredient["severity"] == "safe"
    assert ingredient["trait_flags"] == []
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
        "description": None,
        "comedogenicity": None,
        "irritancy": None,
        "formula": None,
        "molecular_weight": None,
        "cas_no": None,
        "ec_no": None,
        "ph_eur_name": None,
        "functions": [],
        "trait_flags": [],
        "category": "Acids",
        "synonyms": [],
        "credits_remaining": 98,
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
            {
                "name": "Aqua",
                "found": True,
                "severity": "safe",
                "category": "Water",
                "description": None,
                "comedogenicity": None,
                "irritancy": None,
                "formula": None,
                "molecular_weight": None,
                "cas_no": None,
                "ec_no": None,
                "ph_eur_name": None,
                "functions": [],
                "trait_flags": ["fragrance"],
            }
        ],
        "credits_remaining": 97,
    }
    mock_post.return_value = mock_response
    
    client = Dermalytics(api_key="test_key")
    analysis = client.analyze_product(["Aqua", "Glycerin"])
    
    assert analysis["safety_status"] == "safe"
    assert analysis["credits_remaining"] == 97
    assert analysis["ingredients"][0]["trait_flags"] == ["fragrance"]
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

@patch('dermalytics.client.requests.get')
def test_no_key_omits_authorization_and_uses_small_page(mock_get):
    mock_get.return_value = Mock(ok=True, json=lambda: {'data': [], 'pagination': {'limit': 3, 'offset': 0, 'next_offset': None}, 'credits_remaining': 0})
    Dermalytics().search_products('cream')
    assert 'limit=3' in mock_get.call_args[0][0]
    assert 'Authorization' not in mock_get.call_args[1]['headers']


@patch('dermalytics.client.requests.get')
@patch('dermalytics.client.requests.post')
def test_no_key_rejects_large_requests(mock_post, mock_get):
    client = Dermalytics()
    for action in [lambda: client.search_products('cream', limit=4), lambda: client.search_ingredients('Water', offset=3), lambda: client.analyze_product(['Water']*6)]:
        with pytest.raises(ValidationError):
            action()
    mock_post.assert_not_called()
    mock_get.assert_not_called()


@patch('dermalytics.client.requests.get')
def test_invalid_key_never_falls_back_to_anonymous(mock_get):
    mock_get.return_value = Mock(ok=False, status_code=401, reason='Unauthorized', json=lambda: {'error': {'message': 'Invalid key'}})
    with pytest.raises(AuthenticationError):
        Dermalytics('bad').search_products('cream')
    assert mock_get.call_count == 1


@patch('dermalytics.client.requests.get')
def test_signup_link_on_success_and_quota_error(mock_get):
    client = Dermalytics()
    signup = 'https://www.dermalytics.dev/dashboard'
    data = {'data': [], 'pagination': {'limit': 3, 'offset': 0, 'next_offset': None}, 'credits_remaining': 0}
    mock_get.return_value = Mock(ok=True, headers={'X-API-Key-URL': signup}, json=lambda: data)
    client.search_products('cream')
    assert client.signup_url == signup
    mock_get.return_value = Mock(ok=False, status_code=429, reason='Too Many Requests', headers={'X-API-Key-URL': signup}, json=lambda: {'error': {'message': 'Register at ' + signup}})
    with pytest.raises(RateLimitError, match='https://www.dermalytics.dev/dashboard'):
        client.search_products('cream')
    assert client.signup_url == signup
    mock_get.return_value = Mock(ok=True, headers={}, json=lambda: data)
    client.search_products('cream')
    assert client.signup_url is None

# Dermalytics Python SDK

[![PyPI version](https://img.shields.io/pypi/v/dermalytics.svg)](https://pypi.org/project/dermalytics/)
[![Python versions](https://img.shields.io/pypi/pyversions/dermalytics.svg)](https://pypi.org/project/dermalytics/)

Python SDK for the [Dermalytics API](https://dermalytics.dev) - Skincare Ingredient Analysis and Safety Ratings.

## ⚠️ Status

This SDK is currently in **alpha**. The API is functional but may have breaking changes in future versions. Use with caution in production environments.

## Installation

```bash
pip install dermalytics
```

## Quick Start

```python
from dermalytics import Dermalytics

# Initialize the client
client = Dermalytics(api_key="your_api_key_here")

# Get ingredient details
ingredient = client.get_ingredient("niacinamide")
print(ingredient)
# {
#     "name": "niacinamide",
#     "severity": "safe",
#     "description": "...",
#     "comedogenicity": 0,
#     "irritancy": 0,
#     "formula": None,
#     "category": "Vitamins",  # or null
#     "synonyms": ["nicotinamide"],
#     "credits_remaining": 99,
#     "trait_flags": [],
#     # ... cas_no, ec_no, ph_eur_name, functions, etc.
# }

# Analyze a product
analysis = client.analyze_product([
    "Aqua",
    "Glycerin",
    "Niacinamide",
    "Salicylic Acid",
    "Hyaluronic Acid"
])
print(analysis)
# {
#     "safety_status": "safe",
#     "ingredients": [
#         {
#             "name": "Aqua",
#             "found": True,
#             "severity": "safe",
#             "category": "Solvent",
#             # ...same detail fields as lookup
#         }
#     ],
#     "credits_remaining": 99,
# }
```

## API Reference

### `Dermalytics(api_key: str, base_url: Optional[str] = None)`

Initialize the Dermalytics API client.

**Parameters:**
- `api_key` (str): Your Dermalytics API key
- `base_url` (str, optional): Base URL for the API (defaults to `https://api.dermalytics.dev`)

**Raises:**
- `ValidationError`: If API key is missing or invalid

### `get_ingredient(name: str) -> Ingredient`

Get detailed information about a specific ingredient.

**Parameters:**
- `name` (str): The name of the ingredient to look up (e.g., "niacinamide")

**Returns:**
- `Ingredient`: Matches OpenAPI **`IngredientResponse`**: detail fields above, including `trait_flags`, plus `name`, `severity`, `category` (string or `null`), `synonyms`, and `credits_remaining`.

**Raises:**
- `ValidationError`: Invalid input or HTTP **400**
- `AuthenticationError`: HTTP **401** / **403**
- `InsufficientCreditsError`: HTTP **402**
- `NotFoundError`: HTTP **404** (ingredient not found; no credit charged)
- `RateLimitError`: HTTP **429** (if returned by the service)
- `APIError`: Server or other errors (e.g. **500**)

### `analyze_product(ingredients: List[str]) -> ProductAnalysis`

Analyze a complete product formulation.

**Parameters:**
- `ingredients` (List[str]): List of ingredient names in the product

**Returns:**
- `ProductAnalysis`: Matches OpenAPI **`AnalyzeResponse`**: `safety_status` (**Severity**), `ingredients` (array of **`IngredientAnalysis`**, including `trait_flags`), and `credits_remaining`.

**Raises:**
- `ValidationError`: Invalid body or HTTP **400** (no analyze charge on validation error per API docs)
- `AuthenticationError`: HTTP **401** / **403**
- `InsufficientCreditsError`: HTTP **402**
- `RateLimitError`: HTTP **429** (if returned by the service)
- `APIError`: Server or other errors (e.g. **500**)

## Error Handling

The SDK provides comprehensive error handling with specific error classes for different scenarios:

```python
from dermalytics import (
    DermalyticsError,
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

try:
    ingredient = client.get_ingredient("niacinamide")
except NotFoundError:
    print("Ingredient not found")
except AuthenticationError:
    print("Invalid API key")
except InsufficientCreditsError:
    print("Not enough credits")
except RateLimitError:
    print("Rate limit exceeded")
except ValidationError as e:
    print(f"Invalid input: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
except DermalyticsError as e:
    print(f"Dermalytics error: {e.message}")
```

### Error Classes

- `DermalyticsError` - Base error class for all SDK errors
- `APIError` - General API errors (server errors, network issues, invalid responses)
- `AuthenticationError` - Authentication failures (401, 403)
- `InsufficientCreditsError` - Insufficient credits (402)
- `NotFoundError` - Resource not found (404)
- `RateLimitError` - Rate limit exceeded (429)
- `ValidationError` - Invalid request data (400, invalid input parameters)

API error bodies follow **`ErrorResponse`**: nested `error` with at least `code` and `message` (and optional `type`). The client surfaces the message string on the exception.

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dermalytics-dev/dermalytics-python.git
cd dermalytics-python
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black dermalytics tests
```

### Type Checking

```bash
mypy dermalytics
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License allows you to:
- ✅ Use the code commercially
- ✅ Modify the code
- ✅ Distribute the code
- ✅ Use privately
- ✅ Include in proprietary software

You must:
- Include the original copyright notice
- Include the license text

## Links

- [PyPI — dermalytics](https://pypi.org/project/dermalytics/)
- [Dermalytics API Documentation](https://docs.dermalytics.dev)
- [GitHub Repository](https://github.com/dermalytics-dev/dermalytics-python)
- [Issue Tracker](https://github.com/dermalytics-dev/dermalytics-python/issues)

## Support

For support, email support@dermalytics.dev or open an issue on GitHub.

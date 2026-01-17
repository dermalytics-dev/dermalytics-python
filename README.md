# Dermalytics Python SDK

Python SDK for the [Dermalytics API](https://dermalytics.dev) - Skincare Ingredient Analysis and Safety Ratings.

## ⚠️ Status

This SDK is currently in **development** and **alpha testing**. The API is functional but may have breaking changes in future versions. Use with caution in production environments.

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
#     "description": "A form of vitamin B3",
#     "category": {"name": "Vitamins", "slug": "vitamins"},
#     "condition_safeties": [],
#     "synonyms": ["nicotinamide"]
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
#     "ingredients": [...],
#     "warnings": []
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
- `Ingredient`: Dictionary containing:
  - `name` (str): Ingredient name
  - `severity` (str): Safety rating (e.g., "safe", "low_risk", "moderate_risk", "high_risk")
  - `description` (str, optional): Description of the ingredient
  - `category` (dict): Category information with `name` and `slug`
  - `condition_safeties` (list): List of condition-specific safety information
  - `synonyms` (list): List of alternative names for the ingredient

**Raises:**
- `ValidationError`: If the ingredient name is invalid
- `NotFoundError`: If the ingredient is not found
- `AuthenticationError`: If authentication fails
- `RateLimitError`: If rate limit is exceeded
- `APIError`: For other API errors

### `analyze_product(ingredients: List[str]) -> ProductAnalysis`

Analyze a complete product formulation.

**Parameters:**
- `ingredients` (List[str]): List of ingredient names in the product

**Returns:**
- `ProductAnalysis`: Dictionary containing:
  - `safety_status` (str): Overall safety status of the product
  - `ingredients` (list): List of analyzed ingredients with their safety ratings
  - `warnings` (list): List of warnings for specific conditions or interactions

**Raises:**
- `ValidationError`: If the ingredients array is invalid
- `AuthenticationError`: If authentication fails
- `RateLimitError`: If rate limit is exceeded
- `APIError`: For other API errors

## Error Handling

The SDK provides comprehensive error handling with specific error classes for different scenarios:

```python
from dermalytics import (
    DermalyticsError,
    APIError,
    AuthenticationError,
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
- `NotFoundError` - Resource not found (404)
- `RateLimitError` - Rate limit exceeded (429)
- `ValidationError` - Invalid request data (400, invalid input parameters)

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

- [Dermalytics API Documentation](https://docs.dermalytics.dev)
- [GitHub Repository](https://github.com/dermalytics-dev/dermalytics-python)
- [Issue Tracker](https://github.com/dermalytics-dev/dermalytics-python/issues)
- [PyPI Package](https://pypi.org/project/dermalytics/)

## Support

For support, email support@dermalytics.dev or open an issue on GitHub.

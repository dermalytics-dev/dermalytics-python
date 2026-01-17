# Dermalytics Python SDK

Python SDK for the [Dermalytics API](https://dermalytics.dev) - Skincare Ingredient Analysis and Safety Ratings.

## ⚠️ Status

This SDK is currently a **placeholder**. Full implementation coming soon. All methods will raise `NotImplementedError` until the SDK is fully implemented.

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

# Analyze a product
analysis = client.analyze_product([
    "Aqua",
    "Glycerin",
    "Niacinamide",
    "Salicylic Acid",
    "Hyaluronic Acid"
])
print(analysis)
```

## API Reference

### `Dermalytics(api_key: str, base_url: Optional[str] = None)`

Initialize the Dermalytics API client.

**Parameters:**
- `api_key` (str): Your Dermalytics API key
- `base_url` (str, optional): Base URL for the API (defaults to `https://api.dermalytics.dev`)

**Raises:**
- `NotImplementedError`: This SDK is currently a placeholder

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
- `NotImplementedError`: This SDK is currently a placeholder
- `NotFoundError`: If the ingredient is not found
- `APIError`: If the API returns an error

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
- `NotImplementedError`: This SDK is currently a placeholder
- `ValidationError`: If the request is invalid
- `APIError`: If the API returns an error

## Error Handling

The SDK provides custom exception classes:

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
except APIError as e:
    print(f"API error: {e}")
```

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

## Publishing to PyPI

### Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Install build tools:
```bash
pip install build twine
```

3. Configure credentials in `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-your-api-token-here
```

### Build and Upload

1. Update version in `setup.py` and `pyproject.toml`

2. Build the package:
```bash
python -m build
```

3. Check the build:
```bash
twine check dist/*
```

4. Upload to PyPI:
```bash
twine upload dist/*
```

5. Upload to TestPyPI (for testing):
```bash
twine upload --repository testpypi dist/*
```

### Version Management

Update the version in both:
- `setup.py`: `version="0.1.0"`
- `pyproject.toml`: `version = "0.1.0"`
- `dermalytics/__init__.py`: `__version__ = "0.1.0"`

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `1.0.0`)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

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

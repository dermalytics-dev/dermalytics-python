# Dermalytics Python SDK

Search cosmetic products and ingredients, retrieve INCI lists, and analyze ingredient data with a typed Python client.

[Documentation](https://www.dermalytics.dev/docs) · [Get an API key](https://www.dermalytics.dev/dashboard) · [OpenAPI](https://api.dermalytics.dev/openapi.json)

## Install

```sh
pip install dermalytics
```

Requires Python 3.8 or later. Keep your API key in an environment variable rather than in source code.

## Try without an API key

```python
from dermalytics import Dermalytics

client = Dermalytics()
matches = client.search_ingredients("Niacinamide")
print(matches["data"])
```

Try the REST API without an API key: **5 requests per IP address in a 24-hour window**, starting with the first request. Search returns up to 3 results, with no pagination; analysis accepts up to 5 ingredient names. The quota is shared across all REST data methods. Empty results and invalid requests that reach the API also use an attempt.

Responses keep the same fields. Without an account, `credits_remaining` is `0`; it is not your free-request balance. HTTP headers `X-Free-Requests-Remaining` and `X-Free-Requests-Reset` report the remaining attempts and reset time (Unix seconds). HTTP 429 includes `Retry-After`. Get a key from the [dashboard](https://www.dermalytics.dev/dashboard) for full access and 100 welcome credits. Supplying an invalid key returns an authentication error; it never falls back to free access. Shared IP addresses share a quota; IPv6 addresses within a /64 share one bucket.

After the second keyless request, `client.signup_url` contains the registration URL. When the quota is exhausted, `RateLimitError` also includes the link in its message. The SDK does not open a browser or print unsolicited messages.

## Use an API key

Set `DERMALYTICS_API_KEY` in your environment, then run:

```python
import os
from dermalytics import Dermalytics

client = Dermalytics(api_key=os.environ["DERMALYTICS_API_KEY"])

page = client.search_products("cream", ingredient="Niacinamide", limit=5)

for product in page["data"]:
    print(product["id"], product["name"], product["brand"])

if page["data"]:
    product = client.get_product(page["data"][0]["id"])
    print(product["ingredients"])
    print("Credits remaining:", product["credits_remaining"])
```

The examples below use this `client`. Its default base URL is `https://api.dermalytics.dev`; set `base_url` in the constructor to use another deployment. Requests are synchronous and use a 30-second HTTP timeout.

## Methods and credits

Responses are dictionaries with type annotations. Successful responses include `credits_remaining`.

| Method | Returns | Credits |
| --- | --- | --- |
| `search_ingredients(query, *, limit=None, offset=0)` | `IngredientSearchResponse` | 1 per non-empty page |
| `get_ingredient(name)` | `Ingredient` | 1 per successful lookup |
| `search_products(query, *, limit=None, offset=0, brand=None, ingredient=None)` | `ProductSearchResponse` | 1 per non-empty page |
| `get_product(product_id)` | `ProductResponse` | 1 per successful lookup |
| `analyze_product(ingredients)` | `ProductAnalysis` | 1 per matched ingredient row |

For requests with an API key, empty search pages, missing records and validation errors do not consume credits. Product lookup accepts a UUID returned by product search.

## Search ingredients

```python
matches = client.search_ingredients("niacinamide", limit=10)
by_cas = client.search_ingredients("98-92-0")
ingredient = client.get_ingredient("Niacinamide")

print(matches["data"])
print(by_cas["data"])
print(ingredient["functions"], ingredient["trait_flags"])
```

## Search products and paginate

```python
query = "cream"
first_page = client.search_products(
    query, brand="CeraVe", ingredient="Niacinamide", limit=10
)

# Fetch one additional page when needed. Each non-empty page costs 1 credit.
next_offset = first_page["pagination"]["next_offset"]
if next_offset is not None:
    next_page = client.search_products(
        query,
        brand="CeraVe",
        ingredient="Niacinamide",
        limit=10,
        offset=next_offset,
    )
    print(next_page["data"])
```

Search queries contain 2–100 characters. Ingredient search matches names and synonyms by case-insensitive substring, or CAS/EC numbers exactly. Product search matches product names and brands by case-insensitive substring.

| Option | Default | Accepted values |
| --- | --- | --- |
| `limit` | `20` with a key; `3` without | Integer from 1 to 50 with a key; 1 to 3 without |
| `offset` | `0` | Integer from 0 to 10,000 with a key; `0` without |
| `brand` | Omitted | Exact brand, case-insensitive; 1–255 characters |
| `ingredient` | Omitted | Exact ingredient name or known synonym, case-insensitive; 1–255 characters |

`brand` and `ingredient` apply only to product search. Results are ordered by name, then ID. Each page has `data`, `pagination` (`limit`, `offset`, `next_offset`) and `credits_remaining`. A null `next_offset` means there is no next page within the supported offset range. Requests are never automatically paginated or retried.

## Analyze an ingredient list

```python
analysis = client.analyze_product(["Water", "Glycerin", "Niacinamide"])

for ingredient in analysis["ingredients"]:
    if not ingredient["found"]:
        print("Not found:", ingredient["name"])
        continue
    print(ingredient["name"], ingredient["comedogenicity"], ingredient["irritancy"])

print("Credits remaining:", analysis["credits_remaining"])
```

To analyze a stored product composition, pass `[item["name"] for item in product["ingredients"]]` to `analyze_product`. Check that the list is non-empty before calling it. Product lookup and analysis are separate paid operations.

## Product fields

Product search returns these fields for each result. Product lookup returns the same fields plus the stored ingredient list.

| Field | Meaning |
| --- | --- |
| `id` | Product UUID; pass it to product lookup |
| `name` | Product name |
| `brand` | Brand, or null |
| `category` | Category name, or null |
| `area` | `face`, `eyes`, `lips`, `body`, `hair`, `nails`, or null |
| `ingredients_count` | Number of linked ingredients |
| `traits_cache` | Stored product trait tags |
| `key_ingredient_tags` | Stored key-ingredient tags |
| `ingredients` | Lookup only: entries with `id`, `name` and nullable `position` |

Only active products are returned. A product lookup response also includes `credits_remaining`. Null values mean the information is unavailable; an empty ingredient list means no linked composition is available. Tags describe stored metadata, not independently verified product claims.

## Ingredient and analysis fields

Ingredient search returns `id`, `name`, `cas_no`, `ec_no`, `functions`, `ratings_available` and `record_updated_at`. The availability flags indicate whether comedogenicity and irritancy ratings exist. The timestamp records a database update, not a formulation verification date.

Ingredient lookup returns `name`, `severity`, `category`, `synonyms` and `credits_remaining`, together with these detail fields:

- `comedogenicity`, `irritancy`: nullable ratings from 0 to 5.
- `formula`, `molecular_weight`, `cas_no`, `ec_no`, `ph_eur_name`: nullable identifiers and chemical metadata.
- `functions`, `trait_flags`: lists of cosmetic functions and ingredient tags.
- `description`: nullable text; currently returned as null.

Analysis returns `safety_status`, `ingredients` and `credits_remaining`. Each ingredient row contains `name`, `found`, `severity`, `category` and the detail fields above. Severity values are `safe`, `low_risk`, `moderate_risk` and `high_risk`. Check `found` and the nullable ratings when interpreting results: a missing record or rating is not evidence of safety.

The SDK returns only documented fields, including nested records. The [OpenAPI specification](https://api.dermalytics.dev/openapi.json) defines the HTTP response schemas.

## Handle errors

```python
from dermalytics import DermalyticsError, InsufficientCreditsError, NotFoundError

try:
    ingredient = client.get_ingredient("Niacinamide")
    print(ingredient["name"])
except InsufficientCreditsError:
    print("Add credits in the dashboard before continuing.")
except NotFoundError:
    print("No ingredient matched that name.")
except DermalyticsError as error:
    print(error.message)
```

| Error | When it occurs |
| --- | --- |
| `ValidationError` | Invalid SDK input or HTTP 400 |
| `AuthenticationError` | HTTP 401 or 403 |
| `InsufficientCreditsError` | HTTP 402 |
| `NotFoundError` | HTTP 404 |
| `RateLimitError` | HTTP 429, including the free-request limit |
| `APIError` | Network failure, invalid response or another HTTP error, including 503 when the catalog is unavailable |

All SDK errors inherit from `DermalyticsError`. A failed network request can have reached the server and consumed credits; check the balance before retrying a paid operation.

## Type hints

The package includes `TypedDict` response definitions and a `py.typed` marker for type checkers. Values remain ordinary Python dictionaries.

```python
from dermalytics import ProductSearchResponse

page: ProductSearchResponse = client.search_products("cream", limit=5)
for product in page["data"]:
    print(product["name"])
```

See [all response types](dermalytics/types.py) for ingredient lookup, analysis, product details and pagination.

## Develop

Use a Python version compatible with the development tools in `requirements.txt`.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e . -r requirements.txt
pytest
mypy dermalytics
python -m build
```

## Resources

- [API reference and examples](https://www.dermalytics.dev/docs)
- [Account, API keys and credits](https://www.dermalytics.dev/dashboard)
- [Report an SDK issue](https://github.com/dermalytics-dev/dermalytics-python/issues)
- [MIT license](LICENSE)

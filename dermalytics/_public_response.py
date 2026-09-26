"""Public response allowlist, matching the API and JavaScript SDK."""
import math
from typing import Any, Dict, cast

RESPONSE_FIELDS = {'ingredient': {'name': 'string', 'severity': 'string', 'category': 'string?', 'synonyms': ['string'], 'credits_remaining': 'number', 'description': 'string?', 'comedogenicity': 'number?', 'irritancy': 'number?', 'formula': 'string?', 'molecular_weight': 'number?', 'cas_no': 'string?', 'ec_no': 'string?', 'ph_eur_name': 'string?', 'functions': ['string'], 'trait_flags': ['string']}, 'analysis': {'safety_status': 'string', 'ingredients': [{'name': 'string', 'found': 'boolean', 'severity': 'string', 'category': 'string?', 'description': 'string?', 'comedogenicity': 'number?', 'irritancy': 'number?', 'formula': 'string?', 'molecular_weight': 'number?', 'cas_no': 'string?', 'ec_no': 'string?', 'ph_eur_name': 'string?', 'functions': ['string'], 'trait_flags': ['string']}], 'credits_remaining': 'number'}, 'ingredientSearch': {'data': [{'id': 'string', 'name': 'string', 'cas_no': 'string?', 'ec_no': 'string?', 'functions': ['string'], 'ratings_available': {'comedogenicity': 'boolean', 'irritancy': 'boolean'}, 'record_updated_at': 'string'}], 'pagination': {'limit': 'number', 'offset': 'number', 'next_offset': 'number?'}, 'credits_remaining': 'number'}, 'productSearch': {'data': [{'id': 'string', 'name': 'string', 'brand': 'string?', 'category': 'string?', 'ingredients_count': 'number', 'area': 'string?', 'traits_cache': ['string'], 'key_ingredient_tags': ['string']}], 'pagination': {'limit': 'number', 'offset': 'number', 'next_offset': 'number?'}, 'credits_remaining': 'number'}, 'product': {'id': 'string', 'name': 'string', 'brand': 'string?', 'category': 'string?', 'ingredients_count': 'number', 'area': 'string?', 'traits_cache': ['string'], 'key_ingredient_tags': ['string'], 'ingredients': [{'id': 'string', 'name': 'string', 'position': 'number?'}], 'credits_remaining': 'number'}}


def _project(value: Any, rule: Any) -> Any:
    if isinstance(rule, str):
        if value is None and rule.endswith("?"):
            return None
        kind = rule.rstrip("?")
        valid = ((kind == "string" and isinstance(value, str)) or
                 (kind == "boolean" and type(value) is bool) or
                 (kind == "number" and type(value) in (int, float) and math.isfinite(value)))
        if not valid:
            raise ValueError("Invalid public response format")
        return value
    if isinstance(rule, list):
        if not isinstance(value, list):
            raise ValueError("Invalid public response format")
        return [_project(item, rule[0]) for item in value]
    if not isinstance(value, dict):
        raise ValueError("Invalid public response format")
    return {key: _project(value[key], child) for key, child in rule.items() if key in value}


def public_response(value: Any, kind: str) -> Dict[str, Any]:
    return cast(Dict[str, Any], _project(value, RESPONSE_FIELDS[kind]))

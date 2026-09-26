"""Regression tests for all SDK response boundaries, including nested unknown fields."""
import json
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from dermalytics import Dermalytics, APIError

CASES = json.loads(Path(__file__).with_name("public-responses.json").read_text())


def invoke(client, kind):
    return {
        "ingredient": lambda: client.get_ingredient("Example"),
        "analysis": lambda: client.analyze_product(["Example"]),
        "ingredientSearch": lambda: client.search_ingredients("Example"),
        "productSearch": lambda: client.search_products("Example"),
        "product": lambda: client.get_product("f879d134-c8e3-4816-a7ad-a042508c44e5"),
    }[kind]()


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["kind"])
@patch("dermalytics.client.requests.post")
@patch("dermalytics.client.requests.get")
def test_only_allowed_fields_leave_sdk(mock_get, mock_post, case):
    original = json.dumps(case["input"])
    response = Mock(ok=True, json=Mock(return_value=case["input"]))
    mock_get.return_value = response
    mock_post.return_value = response
    assert invoke(Dermalytics("test-key"), case["kind"]) == case["expected"]
    assert json.dumps(case["input"]) == original
    assert mock_get.call_count + mock_post.call_count == 1


@pytest.mark.parametrize("body", [
    {"name": {"source": "PRIVATE_MARKER"}},
    {"traits_cache": [{"source": "PRIVATE_MARKER"}]},
    {"ingredients": [{"name": {"source": "PRIVATE_MARKER"}}]},
])
@patch("dermalytics.client.requests.get")
def test_objects_cannot_hide_in_scalar_fields(mock_get, body):
    mock_get.return_value = Mock(ok=True, json=Mock(return_value=body))
    with pytest.raises(APIError, match="Invalid response format"):
        invoke(Dermalytics("test-key"), "product")
    assert mock_get.call_count == 1

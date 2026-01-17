"""Tests for the Dermalytics client."""

import pytest
from dermalytics import Dermalytics


def test_client_initialization():
    """Test that client can be initialized."""
    client = Dermalytics(api_key="test_key")
    assert client is not None
    assert client.api_key == "test_key"
    assert client.base_url == "https://api.dermalytics.dev"


def test_get_ingredient():
    """Test that get_ingredient raises NotImplementedError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(NotImplementedError):
        client.get_ingredient("niacinamide")


def test_analyze_product():
    """Test that analyze_product raises NotImplementedError."""
    client = Dermalytics(api_key="test_key")
    with pytest.raises(NotImplementedError):
        client.analyze_product(["Aqua", "Glycerin"])

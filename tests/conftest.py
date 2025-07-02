"""
Test configuration and fixtures for the Shadowfax Flash API client tests.
"""

import json
from typing import Any, Dict, Optional

import httpx
import pytest
import pytest_asyncio

from shadowfax_flash import Environment, ShadowfaxFlashClient
from shadowfax_flash.models import (
    DropLocationDetails,
    LocationDetails,
    OrderCallbackRequest,
    OrderDetails,
    OrderStatus,
    UserDetails,
)

# Sample test data
TEST_API_KEY = "test_api_key_123"
TEST_CREDITS_KEY = "test_credits_456"
TEST_STORE_BRAND_ID = "test_store_789"
TEST_ORDER_ID = "TEST_ORDER_123"


@pytest_asyncio.fixture
async def mock_httpx_client():
    """Fixture to provide a mocked httpx.AsyncClient."""
    async with httpx.AsyncClient() as client:
        yield client


@pytest_asyncio.fixture
def mock_httpx_response():
    """Fixture to create mocked httpx responses."""

    def _create_response(
        status_code: int = 200,
        json_data: Optional[Dict[str, Any]] = None,
        text: Optional[str] = None,
    ) -> httpx.Response:
        if json_data is not None:
            content = json.dumps(json_data).encode()
            headers = {"content-type": "application/json"}
        else:
            content = text.encode() if text else b""
            headers = {}

        return httpx.Response(
            status_code=status_code,
            content=content,
            headers=headers,
        )

    return _create_response


@pytest_asyncio.fixture
async def test_client(mock_httpx_client):
    """Fixture to create a test client with a test API key and mocked HTTP client."""
    async with ShadowfaxFlashClient(
        api_key=TEST_API_KEY, environment=Environment.STAGING, client=mock_httpx_client
    ) as client:
        yield client


@pytest_asyncio.fixture
def sample_location():
    """Sample location data for testing"""
    return LocationDetails(
        name="Test Location",
        contact_number="9876543210",
        address="123 Test St, Test City",
        latitude=12.9716,
        longitude=77.5946,
    )


@pytest_asyncio.fixture
def sample_drop_location():
    """Sample drop location data for testing"""
    return DropLocationDetails(
        name="Test Drop",
        contact_number="9876543211",
        address="456 Test Ave, Test City",
        latitude=12.9816,
        longitude=77.6046,
    )


@pytest_asyncio.fixture
def sample_order_details():
    """Sample order details for testing"""
    return OrderDetails(
        order_id=TEST_ORDER_ID, is_prepaid=True, cash_to_be_collected=0.0
    )


@pytest_asyncio.fixture
def sample_user_details():
    """Sample user details for testing"""
    return UserDetails(contact_number="9876543210", credits_key=TEST_CREDITS_KEY)


@pytest_asyncio.fixture
def sample_callback_data():
    """Sample callback data for testing"""
    return {
        "coid": TEST_ORDER_ID,
        "status": "DELIVERED",
        "action_time": "2024-01-01T10:00:00Z",
        "rider_id": 1234,
        "rider_contact_number": "9876543212",
        "rider_latitude": 12.9716,
        "rider_longitude": 77.5946,
        "rider_name": "Test Rider",
    }

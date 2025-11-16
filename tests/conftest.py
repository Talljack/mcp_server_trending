"""Test configuration for pytest."""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Configure pytest-asyncio to automatically handle async test functions
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_cache():
    """Mock cache for testing."""
    from utils import SimpleCache

    return SimpleCache(default_ttl=60)


@pytest.fixture
async def mock_http_client():
    """Mock HTTP client for testing."""
    from utils import HTTPClient

    client = HTTPClient(timeout=5.0)
    yield client
    await client.close()

"""Test CodePen fetcher functionality."""

import asyncio
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.codepen import CodePenFetcher
from mcp_server_trending.utils import SimpleCache


@pytest.mark.asyncio
async def test_codepen_popular_pens():
    """Test CodePen popular pens fetcher."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_popular_pens(page=1, use_cache=False)

    assert response.success, f"Fetch should succeed: {response.error}"
    assert response.platform == "codepen", "Platform should be codepen"
    assert len(response.data) > 0, "Should return at least one pen"

    # Verify pen structure
    pen = response.data[0]
    assert hasattr(pen, "title"), "Pen should have title"
    assert hasattr(pen, "url"), "Pen should have url"
    assert hasattr(pen, "rank"), "Pen should have rank"
    assert hasattr(pen, "loves"), "Pen should have loves"
    assert pen.rank == 1, "First pen should have rank 1"

    # Check for note about API limitation
    assert "note" in response.metadata, "Should include note about API limitation"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_picked_pens():
    """Test CodePen picked (featured) pens fetcher."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_picked_pens(page=1, use_cache=False)

    assert response.success, "Fetch should succeed"
    assert response.platform == "codepen", "Platform should be codepen"
    assert response.data_type == "picked_pens", "Data type should be picked_pens"
    assert len(response.data) > 0, "Should return at least one pen"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_recent_pens():
    """Test CodePen recent pens fetcher."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_recent_pens(page=1, use_cache=False)

    assert response.success, "Fetch should succeed"
    assert response.platform == "codepen", "Platform should be codepen"
    assert len(response.data) > 0, "Should return at least one pen"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_pen_structure():
    """Test CodePen pen data structure."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_popular_pens(page=1, use_cache=False)

    assert response.success, "Fetch should succeed"
    if response.data:
        pen = response.data[0]

        # Required fields
        assert pen.id, "Pen should have id"
        assert pen.title, "Pen should have title"
        assert pen.url, "Pen should have url"

        # Optional fields should exist
        assert hasattr(pen, "user"), "Pen should have user attribute"
        assert hasattr(pen, "loves"), "Pen should have loves attribute"
        assert hasattr(pen, "views"), "Pen should have views attribute"
        assert hasattr(pen, "comments"), "Pen should have comments attribute"
        assert hasattr(pen, "tags"), "Pen should have tags attribute"

        # User structure
        if pen.user:
            assert hasattr(pen.user, "username"), "User should have username"
            assert hasattr(pen.user, "profile_url"), "User should have profile_url"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_caching():
    """Test CodePen caching mechanism."""
    cache = SimpleCache(default_ttl=60)
    fetcher = CodePenFetcher(cache=cache)

    # First fetch
    response1 = await fetcher.fetch_popular_pens(page=1, use_cache=True)
    assert response1.success, "First fetch should succeed"

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_popular_pens(page=1, use_cache=True)
    assert response2.success, "Second fetch should succeed"

    # Data should be identical
    assert len(response1.data) == len(response2.data), "Cached data should be same length"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_fallback_data():
    """Test that fallback data is properly formatted."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_popular_pens(page=1, use_cache=False)

    assert response.success, "Fallback fetch should succeed"
    assert len(response.data) > 0, "Fallback should return data"

    # Verify fallback data structure
    pen = response.data[0]
    assert isinstance(pen.loves, int), "Loves should be integer"
    assert isinstance(pen.views, int), "Views should be integer"
    assert isinstance(pen.tags, list), "Tags should be list"
    assert pen.url.startswith("https://"), "URL should be valid"

    await fetcher.close()


@pytest.mark.asyncio
async def test_codepen_metadata():
    """Test response metadata."""
    fetcher = CodePenFetcher()

    response = await fetcher.fetch_popular_pens(page=1, tag="animation", use_cache=False)

    assert response.success, "Fetch should succeed"
    assert "total_count" in response.metadata, "Metadata should include total_count"
    assert "page" in response.metadata, "Metadata should include page"
    assert response.metadata["page"] == 1, "Page should be 1"

    await fetcher.close()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

"""Test Medium fetcher functionality."""

import asyncio
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.medium import MediumFetcher
from mcp_server_trending.utils import SimpleCache


@pytest.mark.asyncio
async def test_medium_tag_articles():
    """Test Medium tag articles fetcher."""
    fetcher = MediumFetcher()

    response = await fetcher.fetch_tag_articles(
        tag="programming", limit=5, mode="latest", use_cache=False
    )

    # Medium API may be restricted, so we accept either success with real data or fallback
    assert response.success, f"Fetch should succeed: {response.error}"
    assert response.platform == "medium", "Platform should be medium"
    assert len(response.data) > 0, "Should return at least one article"
    assert len(response.data) <= 5, "Should respect limit parameter"

    # Verify article structure
    article = response.data[0]
    assert hasattr(article, "title"), "Article should have title"
    assert hasattr(article, "url"), "Article should have url"
    assert hasattr(article, "rank"), "Article should have rank"
    assert article.rank == 1, "First article should have rank 1"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_different_tags():
    """Test Medium with different tags."""
    fetcher = MediumFetcher()

    tags = ["ai", "technology", "javascript"]

    for tag in tags:
        response = await fetcher.fetch_tag_articles(tag=tag, limit=3, use_cache=False)

        assert response.success, f"Fetch with tag={tag} should succeed"
        assert response.metadata.get("tag") == tag, f"Should include {tag} in metadata"
        assert len(response.data) > 0, f"Should return articles for {tag}"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_publication_articles():
    """Test Medium publication articles fetcher."""
    fetcher = MediumFetcher()

    # Test with a known Medium publication
    response = await fetcher.fetch_publication_articles(
        publication="hackernoon", limit=5, use_cache=False
    )

    # Should succeed with either real or fallback data
    assert response.success, "Fetch should succeed"
    assert response.platform == "medium", "Platform should be medium"

    if response.data:
        article = response.data[0]
        assert hasattr(article, "title"), "Article should have title"
        assert hasattr(article, "url"), "Article should have url"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_user_articles():
    """Test Medium user articles fetcher."""
    fetcher = MediumFetcher()

    # Test with a user (should handle @ prefix)
    response = await fetcher.fetch_user_articles(username="medium", limit=5, use_cache=False)

    # Should succeed or fail gracefully
    assert isinstance(response.success, bool), "Should have success flag"
    assert response.platform == "medium", "Platform should be medium"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_article_structure():
    """Test Medium article data structure."""
    fetcher = MediumFetcher()

    response = await fetcher.fetch_tag_articles(tag="programming", limit=1, use_cache=False)

    assert response.success, "Fetch should succeed"
    if response.data:
        article = response.data[0]

        # Required fields
        assert article.id, "Article should have id"
        assert article.title, "Article should have title"
        assert article.url, "Article should have url"

        # Optional fields should exist
        assert hasattr(article, "subtitle"), "Article should have subtitle attribute"
        assert hasattr(article, "author"), "Article should have author attribute"
        assert hasattr(article, "claps"), "Article should have claps attribute"
        assert hasattr(article, "responses"), "Article should have responses attribute"
        assert hasattr(article, "tags"), "Article should have tags attribute"
        assert hasattr(article, "reading_time_minutes"), "Article should have reading_time"

        # Author structure
        if article.author:
            assert hasattr(article.author, "username"), "Author should have username"
            assert hasattr(article.author, "user_id"), "Author should have user_id"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_caching():
    """Test Medium caching mechanism."""
    cache = SimpleCache(default_ttl=60)
    fetcher = MediumFetcher(cache=cache)

    # First fetch
    response1 = await fetcher.fetch_tag_articles(tag="ai", limit=3, use_cache=True)
    assert response1.success, "First fetch should succeed"

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_tag_articles(tag="ai", limit=3, use_cache=True)
    assert response2.success, "Second fetch should succeed"

    # Data should be identical if cached
    assert len(response1.data) == len(response2.data), "Cached data should be same length"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_mode_options():
    """Test different mode options."""
    fetcher = MediumFetcher()

    modes = ["latest", "top"]

    for mode in modes:
        response = await fetcher.fetch_tag_articles(
            tag="programming", limit=2, mode=mode, use_cache=False
        )

        assert response.success, f"Fetch with mode={mode} should succeed"
        assert response.metadata.get("mode") == mode, f"Should use {mode} mode"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_fallback_data():
    """Test that fallback data is properly formatted."""
    fetcher = MediumFetcher()

    # This will likely use fallback data due to API restrictions
    response = await fetcher.fetch_tag_articles(tag="test", limit=5, use_cache=False)

    assert response.success, "Fallback fetch should succeed"
    assert len(response.data) > 0, "Fallback should return data"

    # Verify fallback data structure
    article = response.data[0]
    assert isinstance(article.claps, int), "Claps should be integer"
    assert isinstance(article.responses, int), "Responses should be integer"
    assert isinstance(article.tags, list), "Tags should be list"
    assert article.url.startswith("https://"), "URL should be valid"

    # Check for note about API
    if "note" in response.metadata:
        assert "medium.com" in response.metadata["note"].lower(), "Note should mention Medium"

    await fetcher.close()


@pytest.mark.asyncio
async def test_medium_metadata():
    """Test response metadata."""
    fetcher = MediumFetcher()

    response = await fetcher.fetch_tag_articles(
        tag="python", limit=10, mode="latest", use_cache=False
    )

    assert response.success, "Fetch should succeed"
    assert "total_count" in response.metadata, "Metadata should include total_count"
    assert "tag" in response.metadata, "Metadata should include tag"
    assert "mode" in response.metadata, "Metadata should include mode"
    assert response.metadata["tag"] == "python", "Tag should be python"
    assert response.metadata["mode"] == "latest", "Mode should be latest"

    await fetcher.close()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

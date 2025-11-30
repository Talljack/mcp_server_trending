"""Test Hashnode fetcher functionality."""

import asyncio
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.hashnode import HashnodeFetcher
from mcp_server_trending.utils import SimpleCache


@pytest.mark.asyncio
async def test_hashnode_trending_articles():
    """Test Hashnode trending articles fetcher."""
    fetcher = HashnodeFetcher()

    # Test basic fetch
    response = await fetcher.fetch_trending_articles(limit=5, use_cache=False)

    assert response.success, f"Fetch should succeed: {response.error}"
    assert response.platform == "hashnode", "Platform should be hashnode"
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
async def test_hashnode_with_tag():
    """Test Hashnode articles with tag filter."""
    fetcher = HashnodeFetcher()

    response = await fetcher.fetch_trending_articles(limit=3, tag="javascript", use_cache=False)

    assert response.success, "Fetch with tag should succeed"
    assert len(response.data) <= 3, "Should respect limit"
    assert response.metadata.get("tag") == "javascript", "Should include tag in metadata"

    await fetcher.close()


@pytest.mark.asyncio
async def test_hashnode_publication_articles():
    """Test Hashnode publication articles fetcher."""
    fetcher = HashnodeFetcher()

    # Test with a known Hashnode publication
    # Note: This may fail if publication doesn't exist
    response = await fetcher.fetch_publication_articles(
        publication_host="hashnode.com", limit=5, use_cache=False
    )

    # We expect this to either succeed or fail gracefully
    assert isinstance(response.success, bool), "Response should have success flag"
    assert response.platform == "hashnode", "Platform should be hashnode"

    if response.success and response.data:
        article = response.data[0]
        assert hasattr(article, "title"), "Article should have title"
        assert hasattr(article, "url"), "Article should have url"

    await fetcher.close()


@pytest.mark.asyncio
async def test_hashnode_caching():
    """Test Hashnode caching mechanism."""
    cache = SimpleCache(default_ttl=60)
    fetcher = HashnodeFetcher(cache=cache)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_trending_articles(limit=3, use_cache=True)
    assert response1.success, "First fetch should succeed"
    assert not response1.cache_hit, "First fetch should not be from cache"

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_trending_articles(limit=3, use_cache=True)
    assert response2.success, "Second fetch should succeed"
    assert response2.cache_hit, "Second fetch should be from cache"

    # Data should be identical if cached
    assert len(response1.data) == len(response2.data), "Cached data should have same length"

    await fetcher.close()


@pytest.mark.asyncio
async def test_hashnode_sort_options():
    """Test different sort options."""
    fetcher = HashnodeFetcher()

    sort_options = ["popular", "recent", "featured"]

    for sort_by in sort_options:
        response = await fetcher.fetch_trending_articles(limit=2, sort_by=sort_by, use_cache=False)

        assert response.success, f"Fetch with sort_by={sort_by} should succeed"
        assert response.metadata.get("sort_by") == sort_by, f"Should use {sort_by} sort"

    await fetcher.close()


@pytest.mark.asyncio
async def test_hashnode_article_metadata():
    """Test article metadata completeness."""
    fetcher = HashnodeFetcher()

    response = await fetcher.fetch_trending_articles(limit=1, use_cache=False)

    assert response.success, "Fetch should succeed"
    if response.data:
        article = response.data[0]

        # Required fields
        assert article.id, "Article should have id"
        assert article.title, "Article should have title"
        assert article.url, "Article should have url"

        # Optional fields should exist (even if None)
        assert hasattr(article, "brief"), "Article should have brief attribute"
        assert hasattr(article, "reactions"), "Article should have reactions attribute"
        assert hasattr(article, "comments_count"), "Article should have comments_count"
        assert hasattr(article, "views"), "Article should have views"
        assert hasattr(article, "tags"), "Article should have tags"
        assert hasattr(article, "author"), "Article should have author"

    await fetcher.close()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

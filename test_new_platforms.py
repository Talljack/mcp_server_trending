#!/usr/bin/env python3
"""Test script for new trending platforms."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp_server_trending.fetchers import (
    HashnodeFetcher,
    CodePenFetcher,
    MediumFetcher,
)
from src.mcp_server_trending.utils import SimpleCache


async def test_hashnode():
    """Test Hashnode fetcher."""
    print("\n" + "=" * 60)
    print("Testing Hashnode Fetcher")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = HashnodeFetcher(cache=cache)

    # Test trending articles
    print("\n1. Testing trending articles...")
    response = await fetcher.fetch_trending_articles(limit=5, use_cache=False)
    print(f"✓ Success: {response.success}")
    print(f"✓ Platform: {response.platform}")
    print(f"✓ Articles found: {len(response.data)}")
    if response.data:
        article = response.data[0]
        print(f"✓ First article: {article.title}")
        print(f"  URL: {article.url}")
        print(f"  Reactions: {article.reactions}")


async def test_codepen():
    """Test CodePen fetcher."""
    print("\n" + "=" * 60)
    print("Testing CodePen Fetcher")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = CodePenFetcher(cache=cache)

    # Test popular pens
    print("\n1. Testing popular pens...")
    response = await fetcher.fetch_popular_pens(page=1, use_cache=False)
    print(f"✓ Success: {response.success}")
    print(f"✓ Platform: {response.platform}")
    print(f"✓ Pens found: {len(response.data)}")
    if response.data:
        pen = response.data[0]
        print(f"✓ First pen: {pen.title}")
        print(f"  URL: {pen.url}")
        print(f"  Loves: {pen.loves}")


async def test_medium():
    """Test Medium fetcher."""
    print("\n" + "=" * 60)
    print("Testing Medium Fetcher")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = MediumFetcher(cache=cache)

    # Test tag articles
    print("\n1. Testing tag articles (programming)...")
    response = await fetcher.fetch_tag_articles(tag="programming", limit=5, use_cache=False)
    print(f"✓ Success: {response.success}")
    print(f"✓ Platform: {response.platform}")
    print(f"✓ Articles found: {len(response.data)}")
    if response.data:
        article = response.data[0]
        print(f"✓ First article: {article.title}")
        print(f"  URL: {article.url}")
        print(f"  Claps: {article.claps}")


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP Server Trending - New Platforms Test")
    print("=" * 60)

    try:
        await test_hashnode()
    except Exception as e:
        print(f"✗ Hashnode test failed: {e}")

    try:
        await test_codepen()
    except Exception as e:
        print(f"✗ CodePen test failed: {e}")

    try:
        await test_medium()
    except Exception as e:
        print(f"✗ Medium test failed: {e}")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

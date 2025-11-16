#!/usr/bin/env python3
"""
Simple test to verify the MCP server can start and list tools.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server_trending.fetchers import (
    GitHubTrendingFetcher,
    HackerNewsFetcher,
    ProductHuntFetcher,
)


async def test_fetchers():
    """Test each fetcher independently."""
    print("=" * 60)
    print("Testing MCP Server Trending Fetchers")
    print("=" * 60)

    # Test GitHub Fetcher
    print("\n1. Testing GitHub Trending Fetcher...")
    try:
        async with GitHubTrendingFetcher() as github:
            response = await github.fetch_trending_repositories(
                time_range="daily", language="python", use_cache=True
            )
            if response.success:
                print(f"   ✓ Successfully fetched {len(response.data)} Python repositories")
                if response.data:
                    first_repo = response.data[0]
                    print(f"   Top repo: {first_repo.author}/{first_repo.name}")
                    print(f"   Stars: {first_repo.stars} (+{first_repo.stars_today} today)")
            else:
                print(f"   ✗ Failed: {response.error}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test Hacker News Fetcher
    print("\n2. Testing Hacker News Fetcher...")
    try:
        async with HackerNewsFetcher() as hn:
            response = await hn.fetch_top_stories(limit=10, use_cache=True)
            if response.success:
                print(f"   ✓ Successfully fetched {len(response.data)} top stories")
                if response.data:
                    first_story = response.data[0]
                    print(f"   Top story: {first_story.title}")
                    print(f"   Score: {first_story.score} | Comments: {first_story.descendants}")
            else:
                print(f"   ✗ Failed: {response.error}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test Product Hunt Fetcher
    print("\n3. Testing Product Hunt Fetcher...")
    try:
        async with ProductHuntFetcher() as ph:
            response = await ph.fetch_today(use_cache=True)
            if response.success:
                print(f"   ✓ Successfully fetched {len(response.data)} products")
                if response.data:
                    first_product = response.data[0]
                    print(f"   Top product: {first_product.name}")
                    print(f"   Tagline: {first_product.tagline}")
            else:
                print(f"   ✗ Failed: {response.error}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


async def test_server():
    """Test the MCP server initialization."""
    print("\n\nTesting MCP Server Initialization...")
    try:
        from server import TrendingMCPServer

        server = TrendingMCPServer()
        print("✓ MCP Server initialized successfully")
        print(f"✓ Server name: {server.server.name}")

        # Cleanup
        await server.cleanup()
        print("✓ Server cleanup successful")

    except Exception as e:
        print(f"✗ Server initialization failed: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Run all tests."""
    await test_fetchers()
    await test_server()


if __name__ == "__main__":
    asyncio.run(main())

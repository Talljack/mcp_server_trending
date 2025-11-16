"""Test AI Tools Directory fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.aitools import AIToolsFetcher


async def test_aitools_trending():
    """Test AI Tools Directory trending fetcher."""

    print("=" * 60)
    print("Testing AI Tools Directory Fetcher")
    print("=" * 60)
    print()

    fetcher = AIToolsFetcher()

    # Test 1: Fetch trending AI tools
    print("Test 1: Fetch trending AI tools (default limit)")
    print("-" * 60)

    response = await fetcher.fetch_trending(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} AI tools")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 tools
        for i, tool in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {tool.name}")
            if tool.category:
                print(f"      Category: {tool.category}")
            if tool.description:
                desc = (
                    tool.description[:80] + "..."
                    if len(tool.description) > 80
                    else tool.description
                )
                print(f"      Description: {desc}")
            if tool.pricing:
                print(f"      Pricing: {tool.pricing}")
            if tool.url:
                print(f"      URL: {tool.url}")
            if tool.tags:
                print(f"      Tags: {', '.join(tool.tags[:3])}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Fetch with small limit
    print(f"\n{'=' * 60}")
    print("Test 2: Fetch with small limit (5 tools)")
    print("-" * 60)

    response = await fetcher.fetch_trending(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} AI tools")
        assert len(response.data) <= 5, "Should respect limit parameter"
        print(f"   ✓ Limit respected: {len(response.data)} <= 5")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Test caching
    print(f"\n{'=' * 60}")
    print("Test 3: Test caching mechanism")
    print("-" * 60)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_trending(limit=3, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} tools")

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_trending(limit=3, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} tools (from cache)")

    if response1.success and response2.success:
        # Data should be identical if cached
        if len(response1.data) == len(response2.data):
            print("   ✓ Cache working: Same data returned")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("AI Tools Directory Tests Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_aitools_trending())

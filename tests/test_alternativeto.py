"""Test AlternativeTo fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.alternativeto import AlternativeToFetcher


async def test_alternativeto_trending():
    """Test AlternativeTo trending apps fetcher."""

    print("=" * 60)
    print("Testing AlternativeTo Trending Apps Fetcher")
    print("=" * 60)
    print()

    fetcher = AlternativeToFetcher()

    # Test 1: Fetch trending apps
    print("Test 1: Fetch trending apps (all platforms)")
    print("-" * 60)

    response = await fetcher.fetch_trending(platform="all", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} apps")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 apps
        for i, app in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {app.name}")
            if app.description:
                desc = app.description[:80] + "..." if len(app.description) > 80 else app.description
                print(f"      Description: {desc}")
            print(f"      Likes: {app.likes}")
            print(f"      Platforms: {', '.join(app.platforms[:5])}")
            print(f"      Open Source: {app.is_open_source}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        raise

    # Test 3: Fetch by platform (Windows)
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch Windows apps")
    print("-" * 60)

    response = await fetcher.fetch_trending(platform="windows", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Windows apps")
        print(f"   ✓ Platform filter: {response.metadata.get('platform')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Search alternatives
    print(f"\n{'=' * 60}")
    print("Test 4: Search alternatives (productivity)")
    print("-" * 60)

    response = await fetcher.search_alternatives(query="productivity", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} alternatives")
        print(f"   ✓ Query: {response.metadata.get('query')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} apps, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} apps, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("AlternativeTo Tests Completed!")
    print("=" * 60)


async def main():
    """Run all AlternativeTo tests."""
    await test_alternativeto_trending()

    print(f"\n{'=' * 80}")
    print("✅ ALL ALTERNATIVETO TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


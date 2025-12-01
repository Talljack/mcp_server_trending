"""Test Betalist fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.betalist import BetalistFetcher


async def test_betalist_startups():
    """Test Betalist startups fetcher."""

    print("=" * 60)
    print("Testing Betalist Startups Fetcher")
    print("=" * 60)
    print()

    fetcher = BetalistFetcher()

    # Test 1: Fetch featured startups
    print("Test 1: Fetch featured startups")
    print("-" * 60)

    response = await fetcher.fetch_featured(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} startups")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 startups
        for i, startup in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {startup.name}")
            if startup.tagline:
                print(f"      Tagline: {startup.tagline}")
            print(f"      URL: {startup.url}")
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

    # Test 3: Fetch latest startups
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch latest startups")
    print("-" * 60)

    response = await fetcher.fetch_latest(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} latest startups")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch by topic
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch startups by topic (ai)")
    print("-" * 60)

    response = await fetcher.fetch_by_topic(topic="ai", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} AI startups")
        print(f"   ✓ Topic: {response.metadata.get('topic')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_featured(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} startups, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_featured(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} startups, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Betalist Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Betalist tests."""
    await test_betalist_startups()

    print(f"\n{'=' * 80}")
    print("✅ ALL BETALIST TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


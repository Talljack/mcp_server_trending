"""Test Stack Overflow fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.stackoverflow import StackOverflowFetcher


async def test_stackoverflow_tags():
    """Test Stack Overflow tags fetcher."""

    print("=" * 60)
    print("Testing Stack Overflow Tags Fetcher")
    print("=" * 60)
    print()

    fetcher = StackOverflowFetcher()

    # Test 1: Fetch popular tags
    print("Test 1: Fetch popular tags")
    print("-" * 60)

    response = await fetcher.fetch_tags(sort="popular", limit=15, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tags")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 5 tags
        for i, tag in enumerate(response.data[:5], 1):
            print(f"\n   {i}. {tag.name}")
            print(f"      Question Count: {tag.count:,}")
            print(f"      Has Synonyms: {tag.has_synonyms}")
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

    # Test 3: Fetch tags by activity
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch tags by activity")
    print("-" * 60)

    response = await fetcher.fetch_tags(sort="activity", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tags by activity")
        print(f"   ✓ Sort: {response.metadata.get('sort')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch tags by name
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch tags by name")
    print("-" * 60)

    response = await fetcher.fetch_tags(sort="name", order="asc", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tags by name")
        print(f"   ✓ Order: {response.metadata.get('order')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_tags(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} tags, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_tags(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} tags, cache_hit={response2.cache_hit}")

    # Test 6: Check quota remaining
    print(f"\n{'=' * 60}")
    print("Test 6: Check API quota")
    print("-" * 60)

    if response.metadata.get("quota_remaining"):
        print(f"   ✓ Quota remaining: {response.metadata.get('quota_remaining')}")
    else:
        print(f"   ℹ Quota info not available")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Stack Overflow Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Stack Overflow tests."""
    await test_stackoverflow_tags()

    print(f"\n{'=' * 80}")
    print("✅ ALL STACK OVERFLOW TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


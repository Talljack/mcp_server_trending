"""Test V2EX fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.v2ex import V2EXFetcher


async def test_v2ex_topics():
    """Test V2EX topics fetcher."""

    print("=" * 60)
    print("Testing V2EX Topics Fetcher")
    print("=" * 60)
    print()

    fetcher = V2EXFetcher()

    # Test 1: Fetch hot topics
    print("Test 1: Fetch hot topics")
    print("-" * 60)

    response = await fetcher.fetch_hot_topics(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} topics")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 topics
        for i, topic in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {topic.title}")
            if topic.member_username:
                print(f"      Author: {topic.member_username}")
            if topic.node_title:
                print(f"      Node: {topic.node_title}")
            print(f"      Replies: {topic.replies}")
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

    # Test 3: Fetch latest topics
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch latest topics")
    print("-" * 60)

    response = await fetcher.fetch_latest_topics(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} latest topics")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_hot_topics(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} topics, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_hot_topics(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} topics, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("V2EX Tests Completed!")
    print("=" * 60)


async def main():
    """Run all V2EX tests."""
    await test_v2ex_topics()

    print(f"\n{'=' * 80}")
    print("✅ ALL V2EX TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


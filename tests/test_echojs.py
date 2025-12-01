"""Test Echo JS fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.echojs import EchoJSFetcher


async def test_echojs_news():
    """Test Echo JS news fetcher."""

    print("=" * 60)
    print("Testing Echo JS News Fetcher")
    print("=" * 60)
    print()

    fetcher = EchoJSFetcher()

    # Test 1: Fetch latest news
    print("Test 1: Fetch latest news")
    print("-" * 60)

    response = await fetcher.fetch_latest(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} news items")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 news items
        for i, news in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {news.title}")
            print(f"      Up: {news.up}, Down: {news.down}")
            print(f"      Comments: {news.comments}")
            print(f"      Username: {news.username}")
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

    # Test 3: Fetch top news
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch top news")
    print("-" * 60)

    response = await fetcher.fetch_top(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} top news items")
        print(f"   ✓ Sort: {response.metadata.get('sort')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_latest(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} news, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_latest(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} news, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Echo JS Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Echo JS tests."""
    await test_echojs_news()

    print(f"\n{'=' * 80}")
    print("✅ ALL ECHO JS TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


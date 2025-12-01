"""Test Juejin (掘金) fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.juejin import JuejinFetcher


async def test_juejin_articles():
    """Test Juejin articles fetcher."""

    print("=" * 60)
    print("Testing Juejin (掘金) Articles Fetcher")
    print("=" * 60)
    print()

    fetcher = JuejinFetcher()

    # Test 1: Fetch recommended articles
    print("Test 1: Fetch recommended articles")
    print("-" * 60)

    response = await fetcher.fetch_recommended_articles(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} articles")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 articles
        for i, article in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {article.title}")
            if article.user_name:
                print(f"      Author: {article.user_name}")
            print(f"      Views: {article.view_count}")
            print(f"      Likes: {article.digg_count}")
            print(f"      Comments: {article.comment_count}")
            if article.category_name:
                print(f"      Category: {article.category_name}")
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

    # Test 3: Test caching
    print(f"\n{'=' * 60}")
    print("Test 3: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_recommended_articles(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} articles, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_recommended_articles(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} articles, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Juejin Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Juejin tests."""
    await test_juejin_articles()

    print(f"\n{'=' * 80}")
    print("✅ ALL JUEJIN TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


"""Test dev.to fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.devto import DevToFetcher


async def test_devto_articles():
    """Test dev.to articles fetcher."""

    print("=" * 60)
    print("Testing dev.to Articles Fetcher")
    print("=" * 60)
    print()

    fetcher = DevToFetcher()

    # Test 1: Fetch articles
    print("Test 1: Fetch articles (default)")
    print("-" * 60)

    response = await fetcher.fetch_articles(per_page=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} articles")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 articles
        for i, article in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {article.title}")
            if article.user_name:
                print(f"      Author: {article.user_name}")
            print(f"      Reactions: {article.positive_reactions_count}")
            print(f"      Comments: {article.comments_count}")
            if article.tags:
                print(f"      Tags: {', '.join(article.tags[:5])}")
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

    # Test 3: Fetch articles by tag
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch articles by tag (javascript)")
    print("-" * 60)

    response = await fetcher.fetch_articles(per_page=5, tag="javascript", use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} JavaScript articles")
        print(f"   ✓ Tag filter: {response.metadata.get('tag')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch top articles (weekly)
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch top articles (weekly)")
    print("-" * 60)

    response = await fetcher.fetch_articles(per_page=5, top=7, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} top weekly articles")
        print(f"   ✓ Top: {response.metadata.get('top')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_articles(per_page=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} articles, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_articles(per_page=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} articles, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("dev.to Tests Completed!")
    print("=" * 60)


async def main():
    """Run all dev.to tests."""
    await test_devto_articles()

    print(f"\n{'=' * 80}")
    print("✅ ALL DEV.TO TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


"""Test Lobsters fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.lobsters import LobstersFetcher


async def test_lobsters_stories():
    """Test Lobsters stories fetcher."""

    print("=" * 60)
    print("Testing Lobsters Stories Fetcher")
    print("=" * 60)
    print()

    fetcher = LobstersFetcher()

    # Test 1: Fetch hottest stories
    print("Test 1: Fetch hottest stories")
    print("-" * 60)

    response = await fetcher.fetch_hottest(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} stories")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 stories
        for i, story in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {story.title}")
            print(f"      Score: {story.score}")
            print(f"      Comments: {story.comment_count}")
            print(f"      Submitter: {story.submitter_user}")
            if story.tags:
                print(f"      Tags: {', '.join(story.tags[:5])}")
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

    # Test 3: Fetch newest stories
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch newest stories")
    print("-" * 60)

    response = await fetcher.fetch_newest(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} newest stories")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch stories by tag
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch stories by tag (python)")
    print("-" * 60)

    response = await fetcher.fetch_by_tag(tag="python", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Python stories")
        print(f"   ✓ Tag: {response.metadata.get('tag')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_hottest(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} stories, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_hottest(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} stories, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Lobsters Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Lobsters tests."""
    await test_lobsters_stories()

    print(f"\n{'=' * 80}")
    print("✅ ALL LOBSTERS TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


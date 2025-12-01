"""Test Hacker News fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.hackernews import HackerNewsFetcher


async def test_hackernews_stories():
    """Test Hacker News stories fetcher."""

    print("=" * 60)
    print("Testing Hacker News Stories Fetcher")
    print("=" * 60)
    print()

    fetcher = HackerNewsFetcher()

    # Test 1: Fetch top stories
    print("Test 1: Fetch top stories")
    print("-" * 60)

    response = await fetcher.fetch_stories(story_type="top", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} stories")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 stories
        for i, story in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {story.title}")
            print(f"      Score: {story.score}")
            print(f"      Author: {story.author}")
            print(f"      Comments: {story.descendants}")
            print(f"      URL: {story.url[:60]}..." if len(story.url) > 60 else f"      URL: {story.url}")
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

    # Test 3: Fetch best stories
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch best stories")
    print("-" * 60)

    response = await fetcher.fetch_stories(story_type="best", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} best stories")
        print(f"   ✓ Story type: {response.metadata.get('story_type')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch Ask HN stories
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch Ask HN stories")
    print("-" * 60)

    response = await fetcher.fetch_stories(story_type="ask", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Ask HN stories")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Fetch Show HN stories
    print(f"\n{'=' * 60}")
    print("Test 5: Fetch Show HN stories")
    print("-" * 60)

    response = await fetcher.fetch_stories(story_type="show", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Show HN stories")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 6: Fetch new stories
    print(f"\n{'=' * 60}")
    print("Test 6: Fetch new stories")
    print("-" * 60)

    response = await fetcher.fetch_stories(story_type="new", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} new stories")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 7: Test caching
    print(f"\n{'=' * 60}")
    print("Test 7: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_stories(story_type="top", limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} stories, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_stories(story_type="top", limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} stories, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Hacker News Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Hacker News tests."""
    await test_hackernews_stories()

    print(f"\n{'=' * 80}")
    print("✅ ALL HACKER NEWS TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


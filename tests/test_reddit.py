"""Test Reddit fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.reddit import RedditFetcher


async def test_reddit_subreddit():
    """Test Reddit subreddit fetcher."""

    print("=" * 60)
    print("Testing Reddit Subreddit Fetcher")
    print("=" * 60)
    print()

    fetcher = RedditFetcher()

    # Test 1: Fetch top posts from a subreddit
    print("Test 1: Fetch top posts from r/programming")
    print("-" * 60)

    response = await fetcher.fetch_subreddit_top(
        subreddit="programming", time_range="week", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} posts")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 posts
        for i, post in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {post.title[:60]}..." if len(post.title) > 60 else f"\n   {i}. {post.title}")
            print(f"      Score: {post.score}")
            print(f"      Comments: {post.num_comments}")
            print(f"      Author: {post.author}")
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

    # Test 3: Fetch hot posts
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch hot posts from r/Python")
    print("-" * 60)

    response = await fetcher.fetch_subreddit_hot(
        subreddit="Python", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} hot posts")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch by topic
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch posts by topic (ai)")
    print("-" * 60)

    response = await fetcher.fetch_by_topic(
        topic="ai", sort_by="hot", limit_per_subreddit=3, max_total=10, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} AI-related posts")
        print(f"   ✓ Topic: {response.metadata.get('topic')}")
        print(f"   ✓ Subreddits queried: {response.metadata.get('subreddits_queried', [])[:5]}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_subreddit_top(
        subreddit="programming", limit=3, use_cache=True
    )
    print(f"   ✓ First fetch: {len(response1.data)} posts, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_subreddit_top(
        subreddit="programming", limit=3, use_cache=True
    )
    print(f"   ✓ Second fetch: {len(response2.data)} posts, cache_hit={response2.cache_hit}")

    # Test 6: Check available topics
    print(f"\n{'=' * 60}")
    print("Test 6: Check available predefined topics")
    print("-" * 60)

    topics = list(fetcher.TOPIC_SUBREDDITS.keys())
    print(f"   ✓ Available topics: {', '.join(topics[:10])}")
    print(f"   ✓ Total topics: {len(topics)}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Reddit Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Reddit tests."""
    await test_reddit_subreddit()

    print(f"\n{'=' * 80}")
    print("✅ ALL REDDIT TESTS COMPLETED!")
    print("=" * 80)
    print()
    print("Note: Reddit API requires authentication for full functionality.")
    print("Configure REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET for real data.")


if __name__ == "__main__":
    asyncio.run(main())


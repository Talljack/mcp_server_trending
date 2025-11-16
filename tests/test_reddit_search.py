"""Test Reddit keyword search functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.reddit import RedditFetcher
from mcp_server_trending.utils import SimpleCache


async def test_reddit_search():
    """Test Reddit keyword search with various queries."""

    print("=" * 60)
    print("Testing Reddit Keyword Search")
    print("=" * 60)
    print()

    # Initialize fetcher
    cache = SimpleCache(default_ttl=3600)
    fetcher = RedditFetcher(cache=cache)

    # Test cases with different types of keywords
    test_queries = [
        "machine learning",  # English phrase
        "deep learning",  # Technical term
        "startup funding",  # Business term
        "indie hacker",  # Community term
        "blockchain",  # Single keyword
        "web3",  # Trending tech
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"🔍 Searching for: '{query}'")
        print(f"{'=' * 60}")

        try:
            # Test 1: Search subreddits
            subreddits = await fetcher.search_subreddits(query=query, limit=5)
            print(f"   ✓ Found {len(subreddits)} subreddits: {subreddits}")

            # Test 2: Fetch posts by topic (uses search internally)
            if subreddits:
                response = await fetcher.fetch_by_topic(
                    topic=query,
                    sort_by="hot",
                    time_range="day",
                    limit_per_subreddit=3,
                    max_total=10,
                    use_cache=False,  # Force fresh data for testing
                )

                if response.success and response.data:
                    print(f"   ✓ Fetched {len(response.data)} posts from searched subreddits")
                    print(f"   ✓ Metadata: {response.metadata}")

                    # Show top 2 posts
                    for i, post in enumerate(response.data[:2], 1):
                        print(f"      {i}. [{post.subreddit}] {post.title[:60]}...")
                        print(f"         Score: {post.score} | Comments: {post.num_comments}")
                else:
                    print(f"   ✗ Failed to fetch posts: {response.error}")
            else:
                print("   ⚠ No subreddits found, skipping post fetch")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Small delay to avoid rate limiting
        await asyncio.sleep(1)

    # Test predefined topics still work
    print(f"\n{'=' * 60}")
    print("✓ Testing predefined topics (should NOT trigger search)")
    print(f"{'=' * 60}")

    response = await fetcher.fetch_by_topic(
        topic="ai",  # Predefined topic
        sort_by="hot",
        limit_per_subreddit=2,
        max_total=5,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Predefined topic 'ai' works: {len(response.data)} posts")
        print(f"   ✓ Used subreddits from: {response.metadata.get('topic')}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("✅ All tests completed!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    asyncio.run(test_reddit_search())

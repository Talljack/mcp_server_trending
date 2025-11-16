"""Test new community platforms."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.v2ex import V2EXFetcher
from mcp_server_trending.fetchers.devto import DevToFetcher


async def test_v2ex():
    """Test V2EX fetcher."""
    print("=" * 60)
    print("Testing V2EX Fetcher")
    print("=" * 60)
    print()

    fetcher = V2EXFetcher()

    # Test hot topics
    print("Fetching V2EX hot topics...")
    response = await fetcher.fetch_hot_topics(limit=5, use_cache=False)

    if response.success:
        print(f"✓ Success: Fetched {len(response.data)} topics")
        for i, topic in enumerate(response.data[:3], 1):
            print(f"\n{i}. {topic.title}")
            print(f"   Node: {topic.node_title}")
            print(f"   Author: {topic.member_username}")
            print(f"   Replies: {topic.replies}")
    else:
        print(f"✗ Failed: {response.error}")

    await fetcher.close()
    print("\n" + "=" * 60)


async def test_devto():
    """Test dev.to fetcher."""
    print("Testing dev.to Fetcher")
    print("=" * 60)
    print()

    fetcher = DevToFetcher()

    # Test articles
    print("Fetching dev.to articles...")
    response = await fetcher.fetch_articles(per_page=5, use_cache=False)

    if response.success:
        print(f"✓ Success: Fetched {len(response.data)} articles")
        for i, article in enumerate(response.data[:3], 1):
            print(f"\n{i}. {article.title}")
            print(f"   Author: {article.user_name}")
            print(f"   Reactions: {article.positive_reactions_count}")
            print(f"   Comments: {article.comments_count}")
    else:
        print(f"✗ Failed: {response.error}")

    await fetcher.close()
    print("\n" + "=" * 60)


async def main():
    """Run all tests."""
    await test_v2ex()
    await test_devto()
    print("\nAll platform tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

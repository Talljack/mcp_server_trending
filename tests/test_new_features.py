#!/usr/bin/env python3
"""
Test new features: Indie Hackers Firebase API and Reddit OAuth
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


async def test_indie_hackers_income():
    """Test Indie Hackers income reports using Firebase API"""
    from mcp_server_trending.fetchers.indiehackers import IndieHackersFetcher

    print("🧪 Testing Indie Hackers Income Reports (Firebase API)...")
    fetcher = IndieHackersFetcher()

    response = await fetcher.fetch_income_reports(limit=5, use_cache=False)

    if response.success and response.data:
        print(f"✅ Success! Got {len(response.data)} income reports")
        print(f"Source: {response.metadata.get('source', 'unknown')}")

        # Show top 3
        for i, report in enumerate(response.data[:3], 1):
            print(f"\n{i}. {report.project_name}")
            print(f"   Revenue: {report.revenue}")
            print(f"   Description: {report.description[:80]}...")
            print(f"   URL: {report.project_url}")
    else:
        print(f"⚠️  Failed or no data: {response.error}")

    await fetcher.close()


async def test_reddit_oauth():
    """Test Reddit with OAuth (if credentials configured)"""
    from mcp_server_trending.fetchers.reddit import RedditFetcher

    print("\n🧪 Testing Reddit (OAuth if configured)...")
    fetcher = RedditFetcher()

    # Check if credentials are configured
    if fetcher.client_id and fetcher.client_secret:
        print("✓ Reddit OAuth credentials found")
    else:
        print("⚠️  Reddit OAuth credentials not configured (will use fallback)")
        print("   Configure REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to test OAuth")

    response = await fetcher.fetch_subreddit_hot(subreddit="programming", limit=3, use_cache=False)

    if response.success and response.data:
        method = response.metadata.get("method", "unknown")
        print(f"✅ Success using {method}! Got {len(response.data)} posts")

        # Show posts
        for post in response.data[:3]:
            print(f"\n- {post.title[:80]}")
            print(f"  Score: {post.score} | Comments: {post.num_comments}")
            print(f"  URL: {post.url[:80]}")
    else:
        print(f"⚠️  Failed: {response.error}")

    await fetcher.close()


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing New Features")
    print("=" * 60)

    await test_indie_hackers_income()
    await test_reddit_oauth()

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

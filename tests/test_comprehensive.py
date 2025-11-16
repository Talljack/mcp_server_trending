#!/usr/bin/env python3
"""
Comprehensive test for all platforms
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


async def test_all_platforms():
    """Test all platforms with actual API calls"""
    from mcp_server_trending.server import TrendingMCPServer

    print("🚀 Starting comprehensive platform tests...\n")
    server = TrendingMCPServer()

    tests = [
        (
            "GitHub Trending",
            server.github_fetcher.fetch_trending_repositories,
            {"time_range": "daily"},
        ),
        ("Hacker News", server.hackernews_fetcher.fetch_stories, {"story_type": "top", "limit": 3}),
        ("Product Hunt", server.producthunt_fetcher.fetch_products, {"time_range": "today"}),
        ("Indie Hackers", server.indiehackers_fetcher.fetch_popular_posts, {"limit": 3}),
        # ("Reddit", server.reddit_fetcher.fetch_subreddit_hot, {"subreddit": "programming", "limit": 3}),  # Disabled: Requires API credentials
        ("OpenRouter", server.openrouter_fetcher.fetch_popular_models, {"limit": 3}),
        ("TrustMRR", server.trustmrr_fetcher.fetch_rankings, {"limit": 3}),
        ("AI Tools", server.aitools_fetcher.fetch_trending, {"limit": 3}),
        ("HuggingFace Models", server.huggingface_fetcher.fetch_trending_models, {"limit": 3}),
        ("V2EX", server.v2ex_fetcher.fetch_hot_topics, {"limit": 3}),
        ("Juejin", server.juejin_fetcher.fetch_recommended_articles, {"limit": 3}),
        ("dev.to", server.devto_fetcher.fetch_articles, {"per_page": 3}),
        ("ModelScope Models", server.modelscope_fetcher.fetch_models, {"page_size": 3}),
    ]

    results = {"success": [], "failed": []}

    for platform_name, fetch_func, kwargs in tests:
        try:
            print(f"📊 Testing {platform_name}...", end=" ")
            response = await fetch_func(**kwargs, use_cache=False)

            if response.success and response.data:
                print(f"✅ Success ({len(response.data)} items)")
                results["success"].append(platform_name)
            else:
                error_msg = response.error or "No data returned"
                print(f"⚠️  No data or failed: {error_msg[:80]}")
                results["failed"].append((platform_name, error_msg))
        except Exception as e:
            print(f"❌ Error: {str(e)[:80]}")
            results["failed"].append((platform_name, str(e)))

    print("\n" + "=" * 60)
    print(f"✅ Successful: {len(results['success'])}/{len(tests)}")
    print(f"❌ Failed: {len(results['failed'])}/{len(tests)}")

    if results["failed"]:
        print("\n⚠️  Failed platforms:")
        for platform, error in results["failed"]:
            print(f"  - {platform}: {error[:100]}")

    await server.cleanup()
    print("\n✓ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(test_all_platforms())

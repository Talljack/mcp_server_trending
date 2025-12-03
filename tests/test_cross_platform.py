"""Tests for Cross-Platform search and trending summary."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.cross_platform import CrossPlatformFetcher
from mcp_server_trending.fetchers.github import GitHubTrendingFetcher
from mcp_server_trending.fetchers.hackernews import HackerNewsFetcher
from mcp_server_trending.fetchers.devto import DevToFetcher
from mcp_server_trending.fetchers.lobsters import LobstersFetcher
from mcp_server_trending.fetchers.huggingface import HuggingFaceFetcher
from mcp_server_trending.fetchers.paperswithcode import PapersWithCodeFetcher
from mcp_server_trending.fetchers.v2ex import V2EXFetcher
from mcp_server_trending.fetchers.juejin import JuejinFetcher
from mcp_server_trending.fetchers.betalist import BetalistFetcher
from mcp_server_trending.utils import SimpleCache, setup_logger


async def test_cross_platform_search():
    """Test cross-platform search functionality."""
    print("=" * 70)
    print("Testing Cross-Platform Search")
    print("=" * 70)

    cache = SimpleCache()
    
    # Initialize fetchers
    fetchers = {
        "github": GitHubTrendingFetcher(cache=cache),
        "hackernews": HackerNewsFetcher(cache=cache),
        "devto": DevToFetcher(cache=cache),
        "lobsters": LobstersFetcher(cache=cache),
        "huggingface": HuggingFaceFetcher(cache=cache),
        "v2ex": V2EXFetcher(cache=cache),
        "juejin": JuejinFetcher(cache=cache),
    }
    
    cross_platform = CrossPlatformFetcher(cache=cache, **fetchers)

    # Test 1: Search for "ai" across all platforms
    print("\nTest 1: Search for 'ai' across platforms")
    print("-" * 70)

    response = await cross_platform.search_all_platforms(
        query="ai",
        limit_per_platform=5,
        use_cache=False,
    )

    if response.success and response.data:
        result = response.data[0]
        print(f"   ✓ Query: {result.query}")
        print(f"   ✓ Total results: {result.total_results}")
        print(f"   ✓ Platforms searched: {result.platforms_searched}")
        print(f"   ✓ Results by platform: {result.results_by_platform}")
        print(f"   ✓ Search time: {result.search_time_ms:.0f}ms")
        print(f"\n   Top 5 results:")
        for i, item in enumerate(result.top_results[:5], 1):
            print(f"   {i}. [{item['platform']}] {item['title'][:50]}...")
            print(f"      Score: {item['score']:.2f}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: JSON serialization
    print("\n" + "=" * 70)
    print("Test 2: JSON serialization")
    print("-" * 70)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")

    # Test 3: Search with specific platforms
    print("\n" + "=" * 70)
    print("Test 3: Search 'python' on specific platforms")
    print("-" * 70)

    response = await cross_platform.search_all_platforms(
        query="python",
        platforms=["github", "devto", "hackernews"],
        limit_per_platform=5,
        use_cache=False,
    )

    if response.success and response.data:
        result = response.data[0]
        print(f"   ✓ Platforms searched: {result.platforms_searched}")
        print(f"   ✓ Total results: {result.total_results}")
        print(f"   ✓ Results by platform: {result.results_by_platform}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Caching mechanism
    print("\n" + "=" * 70)
    print("Test 4: Caching mechanism")
    print("-" * 70)

    response1 = await cross_platform.search_all_platforms(
        query="react",
        platforms=["github"],
        limit_per_platform=3,
        use_cache=True,
    )
    print(f"   ✓ First fetch: cache_hit={response1.cache_hit}")

    response2 = await cross_platform.search_all_platforms(
        query="react",
        platforms=["github"],
        limit_per_platform=3,
        use_cache=True,
    )
    print(f"   ✓ Second fetch: cache_hit={response2.cache_hit}")

    print("\n" + "=" * 70)
    print("Cross-Platform Search Tests Completed!")
    print("=" * 70)


async def test_trending_summary():
    """Test trending summary functionality."""
    print("\n" + "=" * 70)
    print("Testing Trending Summary")
    print("=" * 70)

    cache = SimpleCache()
    
    # Initialize fetchers
    fetchers = {
        "github": GitHubTrendingFetcher(cache=cache),
        "hackernews": HackerNewsFetcher(cache=cache),
        "devto": DevToFetcher(cache=cache),
        "lobsters": LobstersFetcher(cache=cache),
        "huggingface": HuggingFaceFetcher(cache=cache),
        "paperswithcode": PapersWithCodeFetcher(cache=cache),
        "betalist": BetalistFetcher(cache=cache),
        "v2ex": V2EXFetcher(cache=cache),
        "juejin": JuejinFetcher(cache=cache),
    }
    
    cross_platform = CrossPlatformFetcher(cache=cache, **fetchers)

    # Test 1: Get full trending summary
    print("\nTest 1: Get trending summary (all platforms)")
    print("-" * 70)

    response = await cross_platform.get_trending_summary(
        items_per_platform=3,
        use_cache=False,
    )

    if response.success and response.data:
        summary = response.data[0]
        print(f"   ✓ Generated at: {summary.generated_at}")
        print(f"   ✓ Total platforms: {summary.total_platforms}")
        print(f"   ✓ Total items: {summary.total_items}")
        print(f"   ✓ Categories: {summary.categories}")
        
        print(f"\n   Platform summaries:")
        for ps in summary.platform_summaries:
            status = "✓" if ps.fetch_success else "✗"
            print(f"   {status} {ps.platform_display_name}: {ps.item_count} items")
            if ps.error_message:
                print(f"      Error: {ps.error_message}")
        
        print(f"\n   Top highlights:")
        for h in summary.top_highlights[:5]:
            print(f"   • {h[:70]}...")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: JSON serialization
    print("\n" + "=" * 70)
    print("Test 2: JSON serialization")
    print("-" * 70)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")

    # Test 3: Summary with specific platforms
    print("\n" + "=" * 70)
    print("Test 3: Trending summary (specific platforms)")
    print("-" * 70)

    response = await cross_platform.get_trending_summary(
        platforms=["github", "hackernews", "huggingface"],
        items_per_platform=5,
        use_cache=False,
    )

    if response.success and response.data:
        summary = response.data[0]
        print(f"   ✓ Platforms included: {len(summary.platform_summaries)}")
        print(f"   ✓ Total items: {summary.total_items}")
        for ps in summary.platform_summaries:
            print(f"   • {ps.platform_display_name}: {ps.item_count} items")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Summary text generation
    print("\n" + "=" * 70)
    print("Test 4: Summary text generation")
    print("-" * 70)

    if response.success and response.data:
        summary = response.data[0]
        print(f"   Generated summary text:")
        print("-" * 50)
        print(summary.summary_text)
        print("-" * 50)
    else:
        print(f"   ✗ No summary text available")

    print("\n" + "=" * 70)
    print("Trending Summary Tests Completed!")
    print("=" * 70)


async def test_search_specific_topics():
    """Test searching for specific trending topics."""
    print("\n" + "=" * 70)
    print("Testing Search for Specific Topics")
    print("=" * 70)

    cache = SimpleCache()
    
    fetchers = {
        "github": GitHubTrendingFetcher(cache=cache),
        "hackernews": HackerNewsFetcher(cache=cache),
        "devto": DevToFetcher(cache=cache),
        "huggingface": HuggingFaceFetcher(cache=cache),
    }
    
    cross_platform = CrossPlatformFetcher(cache=cache, **fetchers)

    topics = ["llm", "rust", "nextjs"]

    for topic in topics:
        print(f"\nSearching for '{topic}':")
        print("-" * 50)

        response = await cross_platform.search_all_platforms(
            query=topic,
            limit_per_platform=3,
            use_cache=False,
        )

        if response.success and response.data:
            result = response.data[0]
            print(f"   Found {result.total_results} results")
            print(f"   By platform: {result.results_by_platform}")
            if result.top_results:
                print(f"   Top result: [{result.top_results[0]['platform']}] {result.top_results[0]['title'][:40]}...")
        else:
            print(f"   Failed: {response.error}")

    print("\n" + "=" * 70)
    print("Topic Search Tests Completed!")
    print("=" * 70)


async def main():
    """Run all cross-platform tests."""
    setup_logger()

    await test_cross_platform_search()
    await test_trending_summary()
    await test_search_specific_topics()

    print("\n" + "=" * 80)
    print("✅ ALL CROSS-PLATFORM TESTS COMPLETED!")
    print("=" * 80)
    print("\nNew tools available:")
    print("  • search_trending_all - Cross-platform search")
    print("  • get_trending_summary - Today's trending summary")


if __name__ == "__main__":
    asyncio.run(main())


"""Test Indie Hackers fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.indiehackers import IndieHackersFetcher


async def test_indiehackers_posts():
    """Test Indie Hackers popular posts fetcher."""

    print("=" * 60)
    print("Testing Indie Hackers Popular Posts Fetcher")
    print("=" * 60)
    print()

    fetcher = IndieHackersFetcher()

    # Test 1: Fetch popular posts
    print("Test 1: Fetch popular posts")
    print("-" * 60)

    response = await fetcher.fetch_popular_posts(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} posts")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 posts
        for i, post in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {post.title}")
            print(f"      Author: {post.author}")
            print(f"      Comments: {post.comments_count}")
            if post.content_preview:
                preview = post.content_preview[:80] + "..." if len(post.content_preview) > 80 else post.content_preview
                print(f"      Preview: {preview}")
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

    response1 = await fetcher.fetch_popular_posts(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} posts, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_popular_posts(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} posts, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Indie Hackers Posts Tests Completed!")
    print("=" * 60)


async def test_indiehackers_income_reports():
    """Test Indie Hackers income reports fetcher."""

    print(f"\n{'=' * 60}")
    print("Testing Indie Hackers Income Reports Fetcher")
    print("=" * 60)
    print()

    fetcher = IndieHackersFetcher()

    # Test 1: Fetch income reports
    print("Test 1: Fetch income reports (highest revenue)")
    print("-" * 60)

    response = await fetcher.fetch_income_reports(
        limit=10, sorting="highest-revenue", use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} income reports")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 reports
        for i, report in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {report.project_name}")
            print(f"      Revenue: {report.revenue}")
            if report.description:
                desc = report.description[:80] + "..." if len(report.description) > 80 else report.description
                print(f"      Description: {desc}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization for income reports")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        raise

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Indie Hackers Income Reports Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Indie Hackers tests."""
    await test_indiehackers_posts()
    await test_indiehackers_income_reports()

    print(f"\n{'=' * 80}")
    print("✅ ALL INDIE HACKERS TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


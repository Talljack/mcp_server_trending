"""Test GitHub Trending fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.github import GitHubTrendingFetcher


async def test_github_trending_repos():
    """Test GitHub trending repositories fetcher."""

    print("=" * 60)
    print("Testing GitHub Trending Repositories Fetcher")
    print("=" * 60)
    print()

    fetcher = GitHubTrendingFetcher()

    # Test 1: Fetch daily trending repos
    print("Test 1: Fetch daily trending repositories")
    print("-" * 60)

    response = await fetcher.fetch_trending_repositories(
        time_range="daily", use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} repositories")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 repos
        for i, repo in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {repo.author}/{repo.name}")
            print(f"      Stars: {repo.stars:,}")
            print(f"      Stars Today: {repo.stars_today:,}")
            if repo.language:
                print(f"      Language: {repo.language}")
            if repo.description:
                desc = repo.description[:80] + "..." if len(repo.description) > 80 else repo.description
                print(f"      Description: {desc}")
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

    # Test 3: Fetch with language filter
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch Python trending repositories")
    print("-" * 60)

    response = await fetcher.fetch_trending_repositories(
        time_range="daily", language="python", use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Python repositories")
        print(f"   ✓ Language filter applied: {response.metadata.get('language')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test weekly time range
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch weekly trending repositories")
    print("-" * 60)

    response = await fetcher.fetch_trending_repositories(
        time_range="weekly", use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} repositories")
        print(f"   ✓ Time range: {response.metadata.get('time_range')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending_repositories(use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} repos, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending_repositories(use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} repos, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("GitHub Trending Repos Tests Completed!")
    print("=" * 60)


async def test_github_trending_developers():
    """Test GitHub trending developers fetcher."""

    print(f"\n{'=' * 60}")
    print("Testing GitHub Trending Developers Fetcher")
    print("=" * 60)
    print()

    fetcher = GitHubTrendingFetcher()

    # Test 1: Fetch daily trending developers
    print("Test 1: Fetch daily trending developers")
    print("-" * 60)

    response = await fetcher.fetch_trending_developers(
        time_range="daily", use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} developers")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 developers
        for i, dev in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {dev.username}")
            if dev.name:
                print(f"      Name: {dev.name}")
            if dev.repo_name:
                print(f"      Popular Repo: {dev.repo_name}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization for developers")
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
    print("GitHub Trending Developers Tests Completed!")
    print("=" * 60)


async def main():
    """Run all GitHub tests."""
    await test_github_trending_repos()
    await test_github_trending_developers()

    print(f"\n{'=' * 80}")
    print("✅ ALL GITHUB TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


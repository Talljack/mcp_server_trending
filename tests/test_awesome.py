"""Test Awesome Lists fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.awesome import AwesomeFetcher


async def test_awesome_lists():
    """Test Awesome Lists fetcher."""

    print("=" * 60)
    print("Testing Awesome Lists Fetcher")
    print("=" * 60)
    print()

    fetcher = AwesomeFetcher()

    # Test 1: Fetch awesome lists by stars
    print("Test 1: Fetch awesome lists (sorted by stars)")
    print("-" * 60)

    response = await fetcher.fetch_awesome_lists(sort="stars", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} awesome lists")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 lists
        for i, awesome_list in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {awesome_list.full_name}")
            print(f"      Stars: {awesome_list.stars:,}")
            print(f"      Forks: {awesome_list.forks:,}")
            if awesome_list.description:
                desc = awesome_list.description[:80] + "..." if len(awesome_list.description) > 80 else awesome_list.description
                print(f"      Description: {desc}")
            if awesome_list.language:
                print(f"      Language: {awesome_list.language}")
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

    # Test 3: Fetch by language
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch Python awesome lists")
    print("-" * 60)

    response = await fetcher.fetch_awesome_lists(
        sort="stars", language="python", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} Python awesome lists")
        print(f"   ✓ Language filter: {response.metadata.get('language')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch by forks
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch awesome lists (sorted by forks)")
    print("-" * 60)

    response = await fetcher.fetch_awesome_lists(sort="forks", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} awesome lists")
        print(f"   ✓ Sort: {response.metadata.get('sort')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_awesome_lists(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} lists, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_awesome_lists(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} lists, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Awesome Lists Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Awesome Lists tests."""
    await test_awesome_lists()

    print(f"\n{'=' * 80}")
    print("✅ ALL AWESOME LISTS TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


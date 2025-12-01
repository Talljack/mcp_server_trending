"""Test npm packages fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.npm import NPMFetcher


async def test_npm_packages():
    """Test npm packages fetcher."""

    print("=" * 60)
    print("Testing npm Packages Fetcher")
    print("=" * 60)
    print()

    fetcher = NPMFetcher()

    # Test 1: Fetch trending packages
    print("Test 1: Fetch trending packages")
    print("-" * 60)

    response = await fetcher.fetch_trending_packages(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} packages")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 packages
        for i, pkg in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {pkg.name}")
            if pkg.description:
                desc = pkg.description[:80] + "..." if len(pkg.description) > 80 else pkg.description
                print(f"      Description: {desc}")
            print(f"      Version: {pkg.version}")
            print(f"      Weekly Downloads: {pkg.downloads_weekly:,}")
            if pkg.author:
                print(f"      Author: {pkg.author}")
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

    # Test 3: Fetch by category (react)
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch React packages")
    print("-" * 60)

    response = await fetcher.fetch_trending_packages(
        category="react", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} React packages")
        print(f"   ✓ Category: {response.metadata.get('category')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch by category (ai)
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch AI packages")
    print("-" * 60)

    response = await fetcher.fetch_trending_packages(
        category="ai", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} AI packages")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending_packages(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} packages, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending_packages(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} packages, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("npm Packages Tests Completed!")
    print("=" * 60)


async def main():
    """Run all npm tests."""
    await test_npm_packages()

    print(f"\n{'=' * 80}")
    print("✅ ALL NPM TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


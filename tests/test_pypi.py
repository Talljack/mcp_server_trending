"""Test PyPI Trending fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.pypi import PyPIFetcher


async def test_pypi_trending():
    """Test PyPI trending packages fetcher."""

    print("=" * 60)
    print("Testing PyPI Trending Fetcher")
    print("=" * 60)
    print()

    fetcher = PyPIFetcher()

    # Test 1: Fetch top packages
    print("Test 1: Fetch top PyPI packages")
    print("-" * 60)

    response = await fetcher.fetch_trending_packages(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} packages")
        print(f"   ✓ Data source: BigQuery public datasets")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 packages
        for i, pkg in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {pkg.name} (Rank: {pkg.rank})")
            if pkg.version:
                print(f"      Version: {pkg.version}")
            if pkg.summary:
                desc = pkg.summary[:80] + "..." if len(pkg.summary) > 80 else pkg.summary
                print(f"      Summary: {desc}")
            if pkg.downloads_last_month:
                print(f"      Downloads (30d): {pkg.downloads_last_month:,}")
            if pkg.author:
                print(f"      Author: {pkg.author}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Category filter
    print("Test 2: Filter by category (django)")
    print("-" * 60)

    response = await fetcher.fetch_trending_packages(
        category="django", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} django-related packages")

        for i, pkg in enumerate(response.data, 1):
            print(f"\n   {i}. {pkg.name}")
            print(f"      Downloads (30d): {pkg.downloads_last_month:,}")
            if pkg.summary:
                desc = pkg.summary[:80] + "..." if len(pkg.summary) > 80 else pkg.summary
                print(f"      Summary: {desc}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Different categories
    print("Test 3: Test different categories")
    print("-" * 60)

    for category in ["data", "web", "testing"]:
        response = await fetcher.fetch_trending_packages(
            category=category, limit=3, use_cache=False
        )

        if response.success:
            print(f"   ✓ {category.capitalize()}: {len(response.data)} packages")
        else:
            print(f"   ✗ {category.capitalize()}: Error")

    print()

    # Cleanup
    await fetcher.close()

    print("=" * 60)
    print("PyPI Trending Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_pypi_trending())

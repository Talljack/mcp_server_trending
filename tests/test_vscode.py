"""Test VS Code Marketplace fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.vscode import VSCodeMarketplaceFetcher


async def test_vscode_extensions():
    """Test VS Code Marketplace extensions fetcher."""

    print("=" * 60)
    print("Testing VS Code Marketplace Extensions Fetcher")
    print("=" * 60)
    print()

    fetcher = VSCodeMarketplaceFetcher()

    # Test 1: Fetch extensions by installs
    print("Test 1: Fetch extensions (sorted by installs)")
    print("-" * 60)

    response = await fetcher.fetch_trending_extensions(
        sort_by="installs", limit=10, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} extensions")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 extensions
        for i, ext in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {ext.extension_name}")
            print(f"      Publisher: {ext.publisher_name}")
            if ext.short_description:
                desc = ext.short_description[:80] + "..." if len(ext.short_description) > 80 else ext.short_description
                print(f"      Description: {desc}")
            print(f"      Installs: {ext.install_count:,}")
            print(f"      Rating: {ext.rating:.1f} ({ext.rating_count} ratings)")
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

    # Test 3: Fetch by rating
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch extensions (sorted by rating)")
    print("-" * 60)

    response = await fetcher.fetch_trending_extensions(
        sort_by="rating", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} extensions")
        print(f"   ✓ Sort by: {response.metadata.get('sort_by')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch trending
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch trending extensions")
    print("-" * 60)

    response = await fetcher.fetch_trending_extensions(
        sort_by="trending", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} trending extensions")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending_extensions(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} extensions, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending_extensions(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} extensions, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("VS Code Marketplace Tests Completed!")
    print("=" * 60)


async def main():
    """Run all VS Code Marketplace tests."""
    await test_vscode_extensions()

    print(f"\n{'=' * 80}")
    print("✅ ALL VS CODE MARKETPLACE TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


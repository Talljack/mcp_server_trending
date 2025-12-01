"""Test Chrome Web Store fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.chrome import ChromeWebStoreFetcher


async def test_chrome_extensions():
    """Test Chrome Web Store extensions fetcher."""

    print("=" * 60)
    print("Testing Chrome Web Store Extensions Fetcher")
    print("=" * 60)
    print()

    fetcher = ChromeWebStoreFetcher()

    # Test 1: Fetch productivity extensions
    print("Test 1: Fetch productivity extensions")
    print("-" * 60)

    response = await fetcher.fetch_trending_extensions(
        category="productivity", limit=10, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} extensions")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 extensions
        for i, ext in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {ext.name}")
            if ext.short_description:
                desc = ext.short_description[:80] + "..." if len(ext.short_description) > 80 else ext.short_description
                print(f"      Description: {desc}")
            print(f"      Rating: {ext.rating}")
            print(f"      Users: {ext.user_count_display}")
            print(f"      Developer: {ext.developer}")
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

    # Test 3: Fetch developer tools extensions
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch developer tools extensions")
    print("-" * 60)

    response = await fetcher.fetch_trending_extensions(
        category="developer-tools", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} developer tools extensions")
        print(f"   ✓ Category: {response.metadata.get('category')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending_extensions(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} extensions, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending_extensions(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} extensions, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Chrome Web Store Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Chrome Web Store tests."""
    await test_chrome_extensions()

    print(f"\n{'=' * 80}")
    print("✅ ALL CHROME WEB STORE TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


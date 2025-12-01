"""Test Product Hunt fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.producthunt import ProductHuntFetcher


async def test_producthunt_products():
    """Test Product Hunt products fetcher."""

    print("=" * 60)
    print("Testing Product Hunt Products Fetcher")
    print("=" * 60)
    print()

    fetcher = ProductHuntFetcher()

    # Test 1: Fetch today's products
    print("Test 1: Fetch today's products")
    print("-" * 60)

    response = await fetcher.fetch_products(time_range="today", use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} products")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 products
        for i, product in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {product.name}")
            if product.tagline:
                print(f"      Tagline: {product.tagline}")
            if product.makers:
                print(f"      Makers: {', '.join(product.makers[:3])}")
            print(f"      URL: {product.url}")
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

    # Test 3: Fetch this week's products
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch this week's products")
    print("-" * 60)

    response = await fetcher.fetch_products(time_range="week", use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} products")
        print(f"   ✓ Time range: {response.metadata.get('time_range')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch this month's products
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch this month's products")
    print("-" * 60)

    response = await fetcher.fetch_products(time_range="month", use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} products")
        print(f"   ✓ Time range: {response.metadata.get('time_range')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_products(time_range="today", use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} products, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_products(time_range="today", use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} products, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Product Hunt Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Product Hunt tests."""
    await test_producthunt_products()

    print(f"\n{'=' * 80}")
    print("✅ ALL PRODUCT HUNT TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


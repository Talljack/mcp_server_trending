"""Tests for Gumroad fetcher."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.gumroad import GumroadFetcher
from mcp_server_trending.utils import SimpleCache, setup_logger


async def test_gumroad_discover():
    """Test fetching products from Gumroad discover page."""
    print("=" * 60)
    print("Testing Gumroad Discover Products")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = GumroadFetcher(cache=cache)

    # Test 1: Fetch featured products
    print("\nTest 1: Fetch featured products (all categories)")
    print("-" * 60)

    response = await fetcher.fetch_discover_products(
        category=None,
        sort="featured",
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} products")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        for product in response.data[:3]:
            d = product.to_dict()
            print(f"\n   {d['rank']}. {d['name']}")
            print(f"      Price: {d['price']}")
            print(f"      Creator: {d['creator']['name']}")
            if d['description']:
                desc = d['description'][:80] + "..." if len(d['description']) > 80 else d['description']
                print(f"      {desc}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: JSON serialization
    print("\n" + "=" * 60)
    print("Test 2: Test JSON serialization")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")

    # Test 3: Caching mechanism
    print("\n" + "=" * 60)
    print("Test 3: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_discover_products(
        category=None,
        sort="featured",
        limit=5,
        use_cache=True,
    )
    print(f"   ✓ First fetch: {len(response1.data)} products, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_discover_products(
        category=None,
        sort="featured",
        limit=5,
        use_cache=True,
    )
    print(f"   ✓ Second fetch: {len(response2.data)} products, cache_hit={response2.cache_hit}")

    print("\n" + "=" * 60)
    print("Gumroad Discover Tests Completed!")
    print("=" * 60)


async def test_gumroad_programming():
    """Test fetching programming products."""
    print("\n" + "=" * 60)
    print("Testing Gumroad Programming Products")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = GumroadFetcher(cache=cache)

    print("\nTest: Fetch programming products")
    print("-" * 60)

    response = await fetcher.fetch_programming_products(
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} programming products")

        for product in response.data[:5]:
            d = product.to_dict()
            print(f"\n   {d['rank']}. {d['name']}")
            print(f"      Price: {d['price']}")
            print(f"      Creator: {d['creator']['name']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Gumroad Programming Tests Completed!")
    print("=" * 60)


async def test_gumroad_design():
    """Test fetching design products."""
    print("\n" + "=" * 60)
    print("Testing Gumroad Design Products")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = GumroadFetcher(cache=cache)

    print("\nTest: Fetch design products")
    print("-" * 60)

    response = await fetcher.fetch_design_products(
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} design products")

        for product in response.data[:5]:
            d = product.to_dict()
            print(f"\n   {d['rank']}. {d['name']}")
            print(f"      Price: {d['price']}")
            print(f"      Creator: {d['creator']['name']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Gumroad Design Tests Completed!")
    print("=" * 60)


async def test_gumroad_search():
    """Test searching for products."""
    print("\n" + "=" * 60)
    print("Testing Gumroad Search")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = GumroadFetcher(cache=cache)

    print("\nTest: Search for 'notion templates'")
    print("-" * 60)

    response = await fetcher.search_products(
        query="notion templates",
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} products")
        print(f"   ✓ Query: {response.metadata.get('query')}")

        for product in response.data[:5]:
            d = product.to_dict()
            print(f"\n   {d['rank']}. {d['name']}")
            print(f"      Price: {d['price']}")
            print(f"      Creator: {d['creator']['name']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Gumroad Search Tests Completed!")
    print("=" * 60)


async def test_gumroad_categories():
    """Test fetching from different categories."""
    print("\n" + "=" * 60)
    print("Testing Gumroad Categories")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = GumroadFetcher(cache=cache)

    categories = ["software", "business", "education"]

    for category in categories:
        print(f"\nTest: Fetch {category} products")
        print("-" * 60)

        response = await fetcher.fetch_category_products(
            category=category,
            limit=5,
            use_cache=False,
        )

        if response.success:
            print(f"   ✓ Success: Fetched {len(response.data)} {category} products")
            if response.data:
                d = response.data[0].to_dict()
                print(f"   ✓ First product: {d['name']} - {d['price']}")
        else:
            print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Gumroad Categories Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Gumroad tests."""
    setup_logger()

    await test_gumroad_discover()
    await test_gumroad_programming()
    await test_gumroad_design()
    await test_gumroad_search()
    await test_gumroad_categories()

    print("\n" + "=" * 80)
    print("✅ ALL GUMROAD TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


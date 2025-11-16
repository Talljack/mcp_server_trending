#!/usr/bin/env python3
"""
Test Product Hunt API integration
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


async def test_producthunt_api():
    """Test Product Hunt API with token"""
    from mcp_server_trending.fetchers.producthunt import ProductHuntFetcher

    print("🧪 Testing Product Hunt GraphQL API...")

    # Check if token is configured
    token = os.getenv("PRODUCTHUNT_API_TOKEN")
    if not token:
        print("⚠️  PRODUCTHUNT_API_TOKEN not configured")
        print("   Set environment variable to test API:")
        print("   export PRODUCTHUNT_API_TOKEN=your_token_here")
        print("\n   Get your token from: https://www.producthunt.com/v2/oauth/applications")
        print("\n   Testing with fallback data...\n")

    fetcher = ProductHuntFetcher()

    # Test fetching today's products
    response = await fetcher.fetch_products(time_range="today", use_cache=False)

    if response.success and response.data:
        source = response.metadata.get("source", "unknown")
        print(f"✅ Success! Got {len(response.data)} products (source: {source})")

        # Show top 3 products
        for i, product in enumerate(response.data[:3], 1):
            print(f"\n{i}. {product.name}")
            print(f"   Tagline: {product.tagline}")
            print(f"   Votes: {product.votes} | Comments: {product.comments_count}")
            if product.topics:
                print(f"   Topics: {', '.join(product.topics[:3])}")
            if product.makers:
                print(f"   Makers: {', '.join(product.makers[:3])}")
            print(f"   URL: {product.url}")
    else:
        error = response.error or "No data returned"
        print(f"❌ Failed: {error}")

    await fetcher.close()


async def main():
    print("=" * 60)
    print("Testing Product Hunt API")
    print("=" * 60 + "\n")

    await test_producthunt_api()

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

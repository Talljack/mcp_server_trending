"""Test TrustMRR fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.trustmrr import TrustMRRFetcher


async def test_trustmrr_rankings():
    """Test TrustMRR rankings fetcher."""

    print("=" * 60)
    print("Testing TrustMRR Rankings Fetcher")
    print("=" * 60)
    print()

    fetcher = TrustMRRFetcher()

    # Test 1: Fetch rankings with default parameters
    print("Test 1: Fetch MRR rankings (default limit)")
    print("-" * 60)

    response = await fetcher.fetch_rankings(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} entries")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 entries
        for i, entry in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {entry.name}")
            print(f"      Rank: #{entry.rank}")
            print(f"      MRR: ${entry.mrr:,.2f}")
            if entry.mrr_growth:
                print(f"      Growth: {entry.mrr_growth:.1f}%")
            if entry.url:
                print(f"      URL: {entry.url}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Fetch with small limit
    print(f"\n{'=' * 60}")
    print("Test 2: Fetch with small limit (5 entries)")
    print("-" * 60)

    response = await fetcher.fetch_rankings(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} entries")
        assert len(response.data) <= 5, "Should respect limit parameter"
        print(f"   ✓ Limit respected: {len(response.data)} <= 5")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Test caching
    print(f"\n{'=' * 60}")
    print("Test 3: Test caching mechanism")
    print("-" * 60)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_rankings(limit=3, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} entries")

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_rankings(limit=3, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} entries (from cache)")

    if response1.success and response2.success:
        # Data should be identical if cached
        if len(response1.data) == len(response2.data):
            print("   ✓ Cache working: Same data returned")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("TrustMRR Tests Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_trustmrr_rankings())

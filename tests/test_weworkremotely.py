"""Test We Work Remotely fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.weworkremotely import WeWorkRemotelyFetcher


async def test_weworkremotely_jobs():
    """Test We Work Remotely jobs fetcher."""

    print("=" * 60)
    print("Testing We Work Remotely Jobs Fetcher")
    print("=" * 60)
    print()

    fetcher = WeWorkRemotelyFetcher()

    # Test 1: Fetch programming jobs
    print("Test 1: Fetch programming jobs")
    print("-" * 60)

    response = await fetcher.fetch_jobs(category="programming", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} jobs")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 jobs
        for i, job in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {job.title}")
            print(f"      Company: {job.company}")
            print(f"      Category: {job.category}")
            if job.region:
                print(f"      Region: {job.region}")
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

    # Test 3: Fetch design jobs
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch design jobs")
    print("-" * 60)

    response = await fetcher.fetch_jobs(category="design", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} design jobs")
        print(f"   ✓ Category: {response.metadata.get('category')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch DevOps jobs
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch DevOps jobs")
    print("-" * 60)

    response = await fetcher.fetch_jobs(category="devops", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} DevOps jobs")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Fetch all jobs
    print(f"\n{'=' * 60}")
    print("Test 5: Fetch all jobs")
    print("-" * 60)

    response = await fetcher.fetch_jobs(category="all", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} jobs (all categories)")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 6: Test caching
    print(f"\n{'=' * 60}")
    print("Test 6: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_jobs(category="programming", limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} jobs, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_jobs(category="programming", limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} jobs, cache_hit={response2.cache_hit}")

    # Test 7: Check available categories
    print(f"\n{'=' * 60}")
    print("Test 7: Check available categories")
    print("-" * 60)

    categories = response.metadata.get("available_categories", [])
    print(f"   ✓ Available categories: {', '.join(categories)}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("We Work Remotely Tests Completed!")
    print("=" * 60)


async def main():
    """Run all We Work Remotely tests."""
    await test_weworkremotely_jobs()

    print(f"\n{'=' * 80}")
    print("✅ ALL WE WORK REMOTELY TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


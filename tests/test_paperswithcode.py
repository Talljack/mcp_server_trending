"""Test Papers with Code fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.paperswithcode import PapersWithCodeFetcher


async def test_paperswithcode_papers():
    """Test Papers with Code papers fetcher."""

    print("=" * 60)
    print("Testing Papers with Code Fetcher")
    print("=" * 60)
    print()

    fetcher = PapersWithCodeFetcher()

    # Test 1: Fetch trending papers
    print("Test 1: Fetch trending papers")
    print("-" * 60)

    response = await fetcher.fetch_trending_papers(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 papers
        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title}")
            if paper.authors:
                print(f"      Authors: {', '.join(paper.authors[:3])}")
            if paper.tasks:
                print(f"      Tasks: {', '.join(paper.tasks[:3])}")
            if paper.arxiv_id:
                print(f"      arXiv ID: {paper.arxiv_id}")
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

    # Test 3: Fetch latest papers
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch latest papers")
    print("-" * 60)

    response = await fetcher.fetch_latest_papers(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} latest papers")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Search papers
    print(f"\n{'=' * 60}")
    print("Test 4: Search papers (transformer)")
    print("-" * 60)

    response = await fetcher.search_papers(query="transformer", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} papers for 'transformer'")
        print(f"   ✓ Query: {response.metadata.get('query')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_trending_papers(limit=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} papers, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_trending_papers(limit=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} papers, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Papers with Code Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Papers with Code tests."""
    await test_paperswithcode_papers()

    print(f"\n{'=' * 80}")
    print("✅ ALL PAPERS WITH CODE TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


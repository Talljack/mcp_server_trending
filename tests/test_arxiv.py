"""Test arXiv Papers fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.arxiv import ArxivFetcher


async def test_arxiv_papers():
    """Test arXiv research papers fetcher."""

    print("=" * 60)
    print("Testing arXiv Papers Fetcher")
    print("=" * 60)
    print()

    fetcher = ArxivFetcher()

    # Test 1: Fetch recent CS papers
    print("Test 1: Fetch recent Computer Science papers")
    print("-" * 60)

    response = await fetcher.fetch_papers(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        print(f"   ✓ Data source: {response.metadata.get('data_source')}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 papers
        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            print(f"      arXiv ID: {paper.arxiv_id}")
            print(f"      Authors: {', '.join(paper.authors[:3])}")
            if len(paper.authors) > 3:
                print(f"               ...and {len(paper.authors) - 3} more")
            print(f"      Category: {paper.primary_category}")
            print(f"      Published: {paper.published[:10]}")
            print(f"      PDF: {paper.pdf_url}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Search by category (cs.AI - Artificial Intelligence)
    print("Test 2: Search AI papers (cs.AI)")
    print("-" * 60)

    response = await fetcher.fetch_papers(category="cs.AI", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} AI papers")

        for i, paper in enumerate(response.data, 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            print(f"      Category: {paper.primary_category}")
            print(f"      Published: {paper.published[:10]}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Search by keywords
    print("Test 3: Search for 'transformers' papers")
    print("-" * 60)

    response = await fetcher.fetch_papers(search_query="transformers", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} papers about transformers")

        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title}")
            if paper.summary:
                summary = paper.summary[:100] + "..." if len(paper.summary) > 100 else paper.summary
                print(f"      Summary: {summary}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 4: Different categories
    print("Test 4: Test different CS categories")
    print("-" * 60)

    for category in ["cs.LG", "cs.CV", "cs.CL"]:
        response = await fetcher.fetch_papers(category=category, limit=3, use_cache=False)

        category_names = {
            "cs.LG": "Machine Learning",
            "cs.CV": "Computer Vision",
            "cs.CL": "Computation and Language (NLP)",
        }

        if response.success:
            print(f"   ✓ {category_names.get(category, category)}: {len(response.data)} papers")
        else:
            print(f"   ✗ {category_names.get(category, category)}: Error")

    print()

    # Cleanup
    await fetcher.close()

    print("=" * 60)
    print("arXiv Papers Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_arxiv_papers())

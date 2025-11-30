"""Test Semantic Scholar fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.semanticscholar import SemanticScholarFetcher


async def test_semanticscholar_papers():
    """Test Semantic Scholar academic papers search."""

    print("=" * 60)
    print("Testing Semantic Scholar Fetcher")
    print("=" * 60)
    print()

    fetcher = SemanticScholarFetcher()

    # Test 1: Search papers by keyword
    print("Test 1: Search for 'deep learning' papers")
    print("-" * 60)

    response = await fetcher.search_papers(
        query="deep learning", sort="citationCount:desc", limit=10, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        print(f"   ✓ Total results: {response.metadata.get('total_results', 'N/A')}")
        print(f"   ✓ Data source: {response.metadata.get('data_source')}")

        # Show top 3 papers
        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title}")
            if paper.authors:
                authors = ", ".join([a.name for a in paper.authors[:3]])
                if len(paper.authors) > 3:
                    authors += f" +{len(paper.authors) - 3} more"
                print(f"      Authors: {authors}")
            print(f"      Year: {paper.year}")
            print(f"      Citations: {paper.citation_count}")
            print(f"      Influential Citations: {paper.influential_citation_count}")
            if paper.venue:
                print(f"      Venue: {paper.venue}")
            if paper.is_open_access:
                print(f"      Open Access: ✓")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Filter by field of study
    print("Test 2: Search Computer Science papers about 'transformers'")
    print("-" * 60)

    response = await fetcher.search_papers(
        query="transformers", fields_of_study=["Computer Science"], limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} CS papers")

        for i, paper in enumerate(response.data, 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            print(f"      Citations: {paper.citation_count}")
            if paper.fields_of_study:
                print(f"      Fields: {', '.join(paper.fields_of_study[:3])}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Filter by year and open access
    print("Test 3: Search recent (2023+) open access papers")
    print("-" * 60)

    response = await fetcher.search_papers(
        query="neural networks", year="2023-2024", open_access_pdf=True, limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} recent open access papers")

        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            print(f"      Year: {paper.year}")
            print(f"      Open Access PDF: {'✓' if paper.open_access_pdf else '✗'}")
            if paper.open_access_pdf:
                print(f"      PDF URL: {paper.open_access_pdf[:60]}...")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 4: Different sorting methods
    print("Test 4: Test different sorting methods")
    print("-" * 60)

    for sort in ["citationCount:desc", "publicationDate:desc"]:
        response = await fetcher.search_papers(
            query="machine learning", sort=sort, limit=3, use_cache=False
        )

        sort_names = {
            "citationCount:desc": "Most Cited",
            "publicationDate:desc": "Most Recent",
        }

        if response.success:
            print(f"   ✓ {sort_names.get(sort, sort)}: {len(response.data)} papers")
        else:
            print(f"   ✗ {sort_names.get(sort, sort)}: Error")

    print()

    # Cleanup
    await fetcher.close()

    print("=" * 60)
    print("Semantic Scholar Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_semanticscholar_papers())

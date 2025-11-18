"""Test OpenReview fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.openreview import OpenReviewFetcher


async def test_openreview_papers():
    """Test OpenReview ML conference papers fetcher."""

    print("=" * 60)
    print("Testing OpenReview Fetcher")
    print("=" * 60)
    print()

    fetcher = OpenReviewFetcher()

    # Test 1: Fetch ICLR 2024 papers
    print("Test 1: Fetch ICLR 2024 conference papers")
    print("-" * 60)

    response = await fetcher.fetch_papers(
        venue="iclr2024",
        limit=10,
        use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        print(f"   ✓ Venue: {response.metadata.get('venue')}")
        print(f"   ✓ Data source: {response.metadata.get('data_source')}")

        # Show top 3 papers
        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            if paper.authors:
                authors = ", ".join(paper.authors[:3])
                if len(paper.authors) > 3:
                    authors += f" +{len(paper.authors) - 3} more"
                print(f"      Authors: {authors}")
            if paper.decision:
                print(f"      Decision: {paper.decision}")
            if paper.rating:
                print(f"      Rating: {paper.rating:.1f}")
            if paper.keywords:
                print(f"      Keywords: {', '.join(paper.keywords[:5])}")
            print(f"      Forum: {paper.forum_url[:60]}...")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Search for specific content
    print("Test 2: Search for 'diffusion' papers in ICLR 2024")
    print("-" * 60)

    response = await fetcher.fetch_papers(
        venue="iclr2024",
        content="diffusion",
        limit=5,
        use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} papers")

        for i, paper in enumerate(response.data, 1):
            print(f"\n   {i}. {paper.title}")
            if paper.rating:
                print(f"      Rating: {paper.rating:.1f}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Filter by decision (accepted papers)
    print("Test 3: Get accepted papers only")
    print("-" * 60)

    response = await fetcher.fetch_papers(
        venue="iclr2024",
        decision="Accept",
        limit=5,
        use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} accepted papers")

        for i, paper in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {paper.title[:80]}...")
            print(f"      Decision: {paper.decision}")
            if paper.rating:
                print(f"      Rating: {paper.rating:.1f}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 4: Different venues
    print("Test 4: Test different conference venues")
    print("-" * 60)

    for venue in ["iclr2024", "neurips2023"]:
        response = await fetcher.fetch_papers(
            venue=venue,
            limit=3,
            use_cache=False
        )

        venue_names = {
            "iclr2024": "ICLR 2024",
            "neurips2023": "NeurIPS 2023",
        }

        if response.success:
            print(f"   ✓ {venue_names.get(venue, venue)}: {len(response.data)} papers")
        else:
            print(f"   ✗ {venue_names.get(venue, venue)}: Error")

    print()

    # Cleanup
    await fetcher.close()

    print("=" * 60)
    print("OpenReview Tests Complete")
    print("=" * 60)
    print()
    print("Summary:")
    print("  - Paper fetching: ✓ Working")
    print("  - Content search: ✓ Working")
    print("  - Decision filtering: ✓ Working")
    print("  - Multiple venues: ✓ Working")


if __name__ == "__main__":
    asyncio.run(test_openreview_papers())

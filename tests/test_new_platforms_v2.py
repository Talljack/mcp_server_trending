"""Test new platforms: Lobsters, Echo JS, We Work Remotely, Papers with Code, AlternativeTo, Replicate, Betalist."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.lobsters import LobstersFetcher
from mcp_server_trending.fetchers.echojs import EchoJSFetcher
from mcp_server_trending.fetchers.weworkremotely import WeWorkRemotelyFetcher
from mcp_server_trending.fetchers.paperswithcode import PapersWithCodeFetcher
from mcp_server_trending.fetchers.alternativeto import AlternativeToFetcher
from mcp_server_trending.fetchers.replicate import ReplicateFetcher
from mcp_server_trending.fetchers.betalist import BetalistFetcher


async def test_lobsters():
    """Test Lobsters fetcher."""
    print("=" * 60)
    print("Testing Lobsters Fetcher")
    print("=" * 60)
    print()

    fetcher = LobstersFetcher()
    success_count = 0
    total_tests = 3

    # Test 1: Hottest stories
    print("1. Fetching Lobsters hottest stories...")
    response = await fetcher.fetch_hottest(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} stories")
        if response.data:
            story = response.data[0]
            print(f"   Sample: {story.title[:50]}...")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Newest stories
    print("\n2. Fetching Lobsters newest stories...")
    response = await fetcher.fetch_newest(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} stories")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Stories by tag
    print("\n3. Fetching Lobsters stories by tag 'python'...")
    response = await fetcher.fetch_by_tag(tag="python", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} stories")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nLobsters: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_echojs():
    """Test Echo JS fetcher."""
    print("\nTesting Echo JS Fetcher")
    print("=" * 60)
    print()

    fetcher = EchoJSFetcher()
    success_count = 0
    total_tests = 2

    # Test 1: Latest news
    print("1. Fetching Echo JS latest news...")
    response = await fetcher.fetch_latest(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} news items")
        if response.data:
            news = response.data[0]
            print(f"   Sample: {news.title[:50]}...")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Top news
    print("\n2. Fetching Echo JS top news...")
    response = await fetcher.fetch_top(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} news items")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nEcho JS: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_weworkremotely():
    """Test We Work Remotely fetcher."""
    print("\nTesting We Work Remotely Fetcher")
    print("=" * 60)
    print()

    fetcher = WeWorkRemotelyFetcher()
    success_count = 0
    total_tests = 2

    # Test 1: Programming jobs
    print("1. Fetching We Work Remotely programming jobs...")
    response = await fetcher.fetch_jobs(category="programming", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} jobs")
        if response.data:
            job = response.data[0]
            print(f"   Sample: {job.title[:50]}... at {job.company}")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: All jobs
    print("\n2. Fetching We Work Remotely all jobs...")
    response = await fetcher.fetch_jobs(category="all", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} jobs")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nWe Work Remotely: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_paperswithcode():
    """Test Papers with Code fetcher."""
    print("\nTesting Papers with Code Fetcher")
    print("=" * 60)
    print()

    fetcher = PapersWithCodeFetcher()
    success_count = 0
    total_tests = 3

    # Test 1: Trending papers
    print("1. Fetching Papers with Code trending papers...")
    response = await fetcher.fetch_trending_papers(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        if response.data:
            paper = response.data[0]
            print(f"   Sample: {paper.title[:50]}...")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Latest papers
    print("\n2. Fetching Papers with Code latest papers...")
    response = await fetcher.fetch_latest_papers(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Search papers
    print("\n3. Searching Papers with Code for 'transformer'...")
    response = await fetcher.search_papers(query="transformer", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} papers")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nPapers with Code: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_alternativeto():
    """Test AlternativeTo fetcher."""
    print("\nTesting AlternativeTo Fetcher")
    print("=" * 60)
    print()

    fetcher = AlternativeToFetcher()
    success_count = 0
    total_tests = 2

    # Test 1: Trending software
    print("1. Fetching AlternativeTo trending software...")
    response = await fetcher.fetch_trending(platform="all", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} apps")
        if response.data:
            app = response.data[0]
            print(f"   Sample: {app.name}")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Search alternatives
    print("\n2. Searching AlternativeTo for 'photoshop' alternatives...")
    response = await fetcher.search_alternatives(query="photoshop", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} alternatives")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nAlternativeTo: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_replicate():
    """Test Replicate fetcher."""
    print("\nTesting Replicate Fetcher")
    print("=" * 60)
    print()

    fetcher = ReplicateFetcher()
    success_count = 0
    total_tests = 2

    # Test 1: Trending models
    print("1. Fetching Replicate trending models...")
    response = await fetcher.fetch_trending_models(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        if response.data:
            model = response.data[0]
            print(f"   Sample: {model.owner}/{model.name}")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Collection models
    print("\n2. Fetching Replicate 'text-to-image' collection...")
    response = await fetcher.fetch_collection(collection="text-to-image", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nReplicate: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def test_betalist():
    """Test Betalist fetcher."""
    print("\nTesting Betalist Fetcher")
    print("=" * 60)
    print()

    fetcher = BetalistFetcher()
    success_count = 0
    total_tests = 3

    # Test 1: Featured startups
    print("1. Fetching Betalist featured startups...")
    response = await fetcher.fetch_featured(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} startups")
        if response.data:
            startup = response.data[0]
            print(f"   Sample: {startup.name}")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Latest startups
    print("\n2. Fetching Betalist latest startups...")
    response = await fetcher.fetch_latest(limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} startups")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Startups by topic
    print("\n3. Fetching Betalist startups by topic 'ai'...")
    response = await fetcher.fetch_by_topic(topic="ai", limit=5, use_cache=False)
    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} startups")
        success_count += 1
    else:
        print(f"   ✗ Failed: {response.error}")

    await fetcher.close()
    print(f"\nBetalist: {success_count}/{total_tests} tests passed")
    print("=" * 60)
    return success_count == total_tests


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("NEW PLATFORMS TEST SUITE")
    print("=" * 60)
    print()

    results = {}

    # Test all platforms
    results["Lobsters"] = await test_lobsters()
    results["Echo JS"] = await test_echojs()
    results["We Work Remotely"] = await test_weworkremotely()
    results["Papers with Code"] = await test_paperswithcode()
    results["AlternativeTo"] = await test_alternativeto()
    results["Replicate"] = await test_replicate()
    results["Betalist"] = await test_betalist()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for platform, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {platform}: {status}")

    print(f"\nTotal: {passed}/{total} platforms passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)


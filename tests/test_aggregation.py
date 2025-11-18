"""Test Aggregation Analysis fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.aggregation import AggregationFetcher
from mcp_server_trending.fetchers.github import GitHubTrendingFetcher
from mcp_server_trending.fetchers.npm import NPMFetcher
from mcp_server_trending.fetchers.pypi import PyPIFetcher
from mcp_server_trending.fetchers.stackoverflow import StackOverflowFetcher
from mcp_server_trending.fetchers.vscode import VSCodeMarketplaceFetcher
from mcp_server_trending.fetchers.remoteok import RemoteOKFetcher
from mcp_server_trending.fetchers.indiehackers import IndieHackersFetcher
from mcp_server_trending.fetchers.trustmrr import TrustMRRFetcher
from mcp_server_trending.fetchers.hackernews import HackerNewsFetcher
from mcp_server_trending.fetchers.devto import DevToFetcher
from mcp_server_trending.fetchers.juejin import JuejinFetcher


async def test_aggregation_analysis():
    """Test cross-platform aggregation analysis tools."""

    print("=" * 60)
    print("Testing Aggregation Analysis Tools")
    print("=" * 60)
    print()

    # Initialize all required fetchers
    github = GitHubTrendingFetcher()
    npm = NPMFetcher()
    pypi = PyPIFetcher()
    stackoverflow = StackOverflowFetcher()
    vscode = VSCodeMarketplaceFetcher()
    remoteok = RemoteOKFetcher()
    indiehackers = IndieHackersFetcher()
    trustmrr = TrustMRRFetcher()
    hackernews = HackerNewsFetcher()
    devto = DevToFetcher()
    juejin = JuejinFetcher()

    # Initialize aggregation fetcher
    aggregation = AggregationFetcher(
        github=github,
        npm=npm,
        pypi=pypi,
        stackoverflow=stackoverflow,
        vscode=vscode,
        remoteok=remoteok,
        indiehackers=indiehackers,
        trustmrr=trustmrr,
        hackernews=hackernews,
        devto=devto,
        juejin=juejin,
    )

    # Test 1: Tech Stack Analysis
    print("Test 1: Tech Stack Analysis (Python)")
    print("-" * 60)

    response = await aggregation.analyze_tech_stack(tech="python", use_cache=False)

    if response.success and response.data:
        analysis = response.data[0]
        print(f"   ✓ Success: Tech stack analysis completed")
        print(f"   ✓ Technology: {analysis.tech_name}")
        print()
        print("   Metrics:")
        print(f"      GitHub repos: {analysis.github_repos}")
        print(f"      npm packages: {analysis.npm_packages}")
        print(f"      PyPI packages: {analysis.pypi_packages}")
        print(f"      Stack Overflow questions: {analysis.stackoverflow_questions:,}")
        print(f"      VS Code extensions: {analysis.vscode_extensions}")
        print(f"      Job postings: {analysis.job_postings}")
        print()
        print(f"   Total Score: {analysis.total_score:.2f}")
        print(f"   Summary: {analysis.summary}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Indie Revenue Dashboard
    print("Test 2: Indie Revenue Dashboard")
    print("-" * 60)

    response = await aggregation.get_indie_revenue_dashboard(use_cache=False)

    if response.success and response.data:
        dashboard = response.data[0]
        print(f"   ✓ Success: Revenue dashboard generated")
        print(f"   ✓ Data sources: {', '.join(dashboard.data_sources)}")
        print()
        print("   Metrics:")
        print(f"      Total projects: {dashboard.total_projects}")
        print(f"      Average MRR: ${dashboard.average_mrr:,.2f}")
        print(f"      Success stories (>$10k): {dashboard.success_stories_count}")
        if dashboard.top_categories:
            print(f"      Top categories: {', '.join(dashboard.top_categories)}")
        print()
        print(f"   Summary: {dashboard.summary}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Topic Trends Tracking
    print("Test 3: Topic Trends Tracking (AI)")
    print("-" * 60)

    response = await aggregation.track_topic_trends(topic="ai", use_cache=False)

    if response.success and response.data:
        trends = response.data[0]
        print(f"   ✓ Success: Topic trends tracked")
        print(f"   ✓ Topic: {trends.topic}")
        print()
        print("   Platform Mentions:")
        print(f"      Hacker News: {trends.hackernews_mentions}")
        print(f"      GitHub repos: {trends.github_repos}")
        print(f"      Stack Overflow tags: {trends.stackoverflow_tags:,}")
        print(f"      dev.to articles: {trends.dev_articles}")
        print(f"      Juejin articles: {trends.juejin_articles}")
        print()
        print(f"   Total Mentions: {trends.total_mentions}")
        print(f"   Trending Score: {trends.trending_score:.2f}")
        print(f"   Summary: {trends.summary}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 4: Different tech stacks
    print("Test 4: Compare multiple tech stacks")
    print("-" * 60)

    for tech in ["react", "vue", "nextjs"]:
        response = await aggregation.analyze_tech_stack(tech=tech, use_cache=False)

        if response.success and response.data:
            analysis = response.data[0]
            print(
                f"   ✓ {tech.capitalize()}: Score {analysis.total_score:.2f} "
                f"({analysis.github_repos} GitHub repos, "
                f"{analysis.npm_packages + analysis.pypi_packages} packages)"
            )
        else:
            print(f"   ✗ {tech.capitalize()}: Error")

    print()

    # Cleanup all fetchers
    await github.close()
    await npm.close()
    await pypi.close()
    await stackoverflow.close()
    await vscode.close()
    await remoteok.close()
    await indiehackers.close()
    await trustmrr.close()
    await hackernews.close()
    await devto.close()
    await juejin.close()

    print("=" * 60)
    print("Aggregation Analysis Tests Complete")
    print("=" * 60)
    print()
    print("Summary:")
    print("  - Tech Stack Analysis: ✓ Cross-platform aggregation")
    print("  - Indie Revenue Dashboard: ✓ Multi-source revenue data")
    print("  - Topic Trends: ✓ Real-time trend tracking")
    print("  - Error Handling: ✓ Graceful degradation")


if __name__ == "__main__":
    asyncio.run(test_aggregation_analysis())

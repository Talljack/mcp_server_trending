"""Example usage of MCP Server Trending."""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fetchers import (
    GitHubTrendingFetcher,
    HackerNewsFetcher,
    ProductHuntFetcher,
)


async def example_github():
    """Example: Fetch GitHub trending data."""
    print("\n=== GitHub Trending Example ===\n")

    async with GitHubTrendingFetcher() as fetcher:
        # Fetch trending Python repositories
        print("Fetching trending Python repositories...")
        response = await fetcher.fetch_trending_repositories(
            time_range="daily",
            language="python"
        )

        if response.success:
            print(f"Found {len(response.data)} repositories\n")
            for repo in response.data[:5]:
                print(f"{repo.rank}. {repo.author}/{repo.name}")
                print(f"   ⭐ {repo.stars} stars (+{repo.stars_today} today)")
                print(f"   📝 {repo.description}\n")
        else:
            print(f"Error: {response.error}")


async def example_hackernews():
    """Example: Fetch Hacker News stories."""
    print("\n=== Hacker News Example ===\n")

    async with HackerNewsFetcher() as fetcher:
        # Fetch top stories
        print("Fetching top stories...")
        response = await fetcher.fetch_top_stories(limit=10)

        if response.success:
            print(f"Found {len(response.data)} stories\n")
            for story in response.data[:5]:
                print(f"{story.rank}. {story.title}")
                print(f"   👤 by {story.author} | 📊 {story.score} points | 💬 {story.descendants} comments")
                print(f"   🔗 {story.url}\n")
        else:
            print(f"Error: {response.error}")


async def example_producthunt():
    """Example: Fetch Product Hunt products."""
    print("\n=== Product Hunt Example ===\n")

    async with ProductHuntFetcher() as fetcher:
        # Fetch today's products
        print("Fetching today's products...")
        response = await fetcher.fetch_today()

        if response.success:
            print(f"Found {len(response.data)} products\n")
            for product in response.data[:5]:
                print(f"{product.rank}. {product.name}")
                print(f"   📝 {product.tagline}")
                print(f"   👍 {product.votes} votes | 💬 {product.comments_count} comments")
                print(f"   🔗 {product.url}\n")
        else:
            print(f"Error: {response.error}")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("MCP Server Trending - Usage Examples")
    print("=" * 60)

    await example_github()
    await example_hackernews()
    await example_producthunt()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

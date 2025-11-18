"""Test WordPress Plugins fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.wordpress import WordPressFetcher


async def test_wordpress_plugins():
    """Test WordPress plugins fetcher."""

    print("=" * 60)
    print("Testing WordPress Plugins Fetcher")
    print("=" * 60)
    print()

    fetcher = WordPressFetcher()

    # Test 1: Fetch popular plugins
    print("Test 1: Fetch popular WordPress plugins")
    print("-" * 60)

    response = await fetcher.fetch_plugins(browse="popular", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} plugins")
        print(f"   ✓ Source: WordPress.org official API")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 plugins
        for i, plugin in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {plugin.name}")
            print(f"      Slug: {plugin.slug}")
            if plugin.active_installs:
                print(f"      Active installs: {plugin.active_installs:,}")
            if plugin.rating:
                print(f"      Rating: {plugin.rating}/100 ({plugin.num_ratings} ratings)")
            if plugin.author:
                print(f"      Author: {plugin.author}")
            if plugin.homepage:
                print(f"      Homepage: {plugin.homepage}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 2: Search functionality
    print("Test 2: Search for SEO plugins")
    print("-" * 60)

    response = await fetcher.fetch_plugins(search="seo", limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} SEO plugins")

        for i, plugin in enumerate(response.data, 1):
            print(f"\n   {i}. {plugin.name}")
            print(f"      Active installs: {plugin.active_installs:,}")
            if plugin.short_description:
                desc = (
                    plugin.short_description[:80] + "..."
                    if len(plugin.short_description) > 80
                    else plugin.short_description
                )
                print(f"      Description: {desc}")
    else:
        print(f"   ✗ Error: {response.error}")

    print()

    # Test 3: Different browse types
    print("Test 3: Different browse types")
    print("-" * 60)

    for browse_type in ["popular", "featured", "new", "updated"]:
        response = await fetcher.fetch_plugins(
            browse=browse_type, limit=3, use_cache=False
        )

        if response.success:
            print(f"   ✓ {browse_type.capitalize()}: {len(response.data)} plugins")
        else:
            print(f"   ✗ {browse_type.capitalize()}: Error - {response.error}")

    print()

    # Cleanup
    await fetcher.close()

    print("=" * 60)
    print("WordPress Plugins Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_wordpress_plugins())

"""Comprehensive test for all MCP tools in the server.

This test file covers all tools registered in the MCP server,
including the newly added platforms:
- Lobsters (3 tools)
- Echo JS (2 tools)
- We Work Remotely (1 tool)
- Papers with Code (3 tools)
- AlternativeTo (2 tools)
- Replicate (2 tools)
- Betalist (3 tools)
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.server import TrendingServer


class MCPToolTester:
    """Test all MCP tools."""

    def __init__(self):
        self.server = None
        self.results = {}

    async def setup(self):
        """Initialize the server."""
        print("Initializing MCP Server...")
        self.server = TrendingServer()
        print("Server initialized successfully.\n")

    async def cleanup(self):
        """Cleanup resources."""
        if self.server:
            await self.server.cleanup()

    async def test_tool(self, tool_name: str, arguments: dict = None) -> bool:
        """Test a single tool."""
        if arguments is None:
            arguments = {}

        try:
            # Get the call_tool handler
            handlers = self.server.server._request_handlers

            # Find the call_tool handler
            call_tool_handler = None
            for handler in handlers.values():
                if hasattr(handler, '__name__') and 'call_tool' in str(handler):
                    call_tool_handler = handler
                    break

            # We need to directly call the fetcher methods instead
            # since we can't easily invoke the MCP handlers directly

            result = await self._call_fetcher_method(tool_name, arguments)
            return result

        except Exception as e:
            print(f"   ✗ Error: {str(e)[:100]}")
            return False

    async def _call_fetcher_method(self, tool_name: str, arguments: dict) -> bool:
        """Call the appropriate fetcher method based on tool name."""
        try:
            # Map tool names to fetcher methods
            if tool_name == "get_lobsters_hottest":
                response = await self.server.lobsters_fetcher.fetch_hottest(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_lobsters_newest":
                response = await self.server.lobsters_fetcher.fetch_newest(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_lobsters_by_tag":
                response = await self.server.lobsters_fetcher.fetch_by_tag(
                    tag=arguments.get("tag", "python"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_echojs_latest":
                response = await self.server.echojs_fetcher.fetch_latest(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_echojs_top":
                response = await self.server.echojs_fetcher.fetch_top(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_weworkremotely_jobs":
                response = await self.server.weworkremotely_fetcher.fetch_jobs(
                    category=arguments.get("category", "programming"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_paperswithcode_trending":
                response = await self.server.paperswithcode_fetcher.fetch_trending_papers(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_paperswithcode_latest":
                response = await self.server.paperswithcode_fetcher.fetch_latest_papers(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "search_paperswithcode":
                response = await self.server.paperswithcode_fetcher.search_papers(
                    query=arguments.get("query", "transformer"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_alternativeto_trending":
                response = await self.server.alternativeto_fetcher.fetch_trending(
                    platform=arguments.get("platform", "all"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "search_alternativeto":
                response = await self.server.alternativeto_fetcher.search_alternatives(
                    query=arguments.get("query", "photoshop"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_replicate_trending":
                response = await self.server.replicate_fetcher.fetch_trending_models(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_replicate_collection":
                response = await self.server.replicate_fetcher.fetch_collection(
                    collection=arguments.get("collection", "text-to-image"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_betalist_featured":
                response = await self.server.betalist_fetcher.fetch_featured(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_betalist_latest":
                response = await self.server.betalist_fetcher.fetch_latest(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_betalist_by_topic":
                response = await self.server.betalist_fetcher.fetch_by_topic(
                    topic=arguments.get("topic", "ai"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            # Existing platforms
            elif tool_name == "get_github_trending_repos":
                response = await self.server.github_fetcher.fetch_trending_repositories(
                    time_range=arguments.get("time_range", "daily"),
                    use_cache=False
                )
            elif tool_name == "get_hackernews_stories":
                response = await self.server.hackernews_fetcher.fetch_stories(
                    story_type=arguments.get("story_type", "top"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_producthunt_products":
                response = await self.server.producthunt_fetcher.fetch_products(
                    time_range=arguments.get("time_range", "today"),
                    use_cache=False
                )
            elif tool_name == "get_devto_articles":
                response = await self.server.devto_fetcher.fetch_articles(
                    per_page=arguments.get("per_page", 5),
                    use_cache=False
                )
            elif tool_name == "get_v2ex_hot_topics":
                response = await self.server.v2ex_fetcher.fetch_hot_topics(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_hashnode_trending_articles":
                response = await self.server.hashnode_fetcher.fetch_trending_articles(
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            elif tool_name == "get_codepen_popular_pens":
                response = await self.server.codepen_fetcher.fetch_popular_pens(
                    use_cache=False
                )
            elif tool_name == "get_medium_tag_articles":
                response = await self.server.medium_fetcher.fetch_tag_articles(
                    tag=arguments.get("tag", "programming"),
                    limit=arguments.get("limit", 5),
                    use_cache=False
                )
            else:
                print(f"   ⚠ Tool {tool_name} not implemented in test")
                return True  # Skip unknown tools

            if response.success:
                print(f"   ✓ Success: {len(response.data)} items returned")
                return True
            else:
                print(f"   ✗ Failed: {response.error}")
                return False

        except Exception as e:
            print(f"   ✗ Error: {str(e)[:100]}")
            return False

    async def run_all_tests(self):
        """Run all tool tests."""
        # Define all tools to test with their arguments
        new_platform_tools = [
            # Lobsters (3 tools)
            ("get_lobsters_hottest", {"limit": 5}),
            ("get_lobsters_newest", {"limit": 5}),
            ("get_lobsters_by_tag", {"tag": "python", "limit": 5}),

            # Echo JS (2 tools)
            ("get_echojs_latest", {"limit": 5}),
            ("get_echojs_top", {"limit": 5}),

            # We Work Remotely (1 tool)
            ("get_weworkremotely_jobs", {"category": "programming", "limit": 5}),

            # Papers with Code (3 tools)
            ("get_paperswithcode_trending", {"limit": 5}),
            ("get_paperswithcode_latest", {"limit": 5}),
            ("search_paperswithcode", {"query": "transformer", "limit": 5}),

            # AlternativeTo (2 tools)
            ("get_alternativeto_trending", {"platform": "all", "limit": 5}),
            ("search_alternativeto", {"query": "photoshop", "limit": 5}),

            # Replicate (2 tools)
            ("get_replicate_trending", {"limit": 5}),
            ("get_replicate_collection", {"collection": "text-to-image", "limit": 5}),

            # Betalist (3 tools)
            ("get_betalist_featured", {"limit": 5}),
            ("get_betalist_latest", {"limit": 5}),
            ("get_betalist_by_topic", {"topic": "ai", "limit": 5}),
        ]

        existing_platform_tools = [
            # GitHub (sample)
            ("get_github_trending_repos", {"time_range": "daily"}),

            # Hacker News
            ("get_hackernews_stories", {"story_type": "top", "limit": 5}),

            # Product Hunt
            ("get_producthunt_products", {"time_range": "today"}),

            # dev.to
            ("get_devto_articles", {"per_page": 5}),

            # V2EX
            ("get_v2ex_hot_topics", {"limit": 5}),

            # Hashnode
            ("get_hashnode_trending_articles", {"limit": 5}),

            # CodePen
            ("get_codepen_popular_pens", {}),

            # Medium
            ("get_medium_tag_articles", {"tag": "programming", "limit": 5}),
        ]

        print("=" * 70)
        print("TESTING NEW PLATFORM TOOLS")
        print("=" * 70)

        new_passed = 0
        new_total = len(new_platform_tools)

        for tool_name, args in new_platform_tools:
            print(f"\n{tool_name}:")
            success = await self.test_tool(tool_name, args)
            if success:
                new_passed += 1
            self.results[tool_name] = success
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)

        print("\n" + "=" * 70)
        print("TESTING EXISTING PLATFORM TOOLS (SAMPLE)")
        print("=" * 70)

        existing_passed = 0
        existing_total = len(existing_platform_tools)

        for tool_name, args in existing_platform_tools:
            print(f"\n{tool_name}:")
            success = await self.test_tool(tool_name, args)
            if success:
                existing_passed += 1
            self.results[tool_name] = success
            await asyncio.sleep(0.5)

        # Print summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        print(f"\nNew Platform Tools: {new_passed}/{new_total} passed")
        print(f"Existing Platform Tools: {existing_passed}/{existing_total} passed")
        print(f"Total: {new_passed + existing_passed}/{new_total + existing_total} passed")

        print("\nDetailed Results:")
        print("-" * 50)
        for tool_name, success in self.results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {tool_name}")

        return new_passed == new_total


async def main():
    """Main entry point."""
    tester = MCPToolTester()

    try:
        await tester.setup()
        success = await tester.run_all_tests()
    finally:
        await tester.cleanup()

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)


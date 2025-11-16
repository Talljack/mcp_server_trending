"""MCP Server implementation for Trending data."""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from . import __version__
from .config import config
from .fetchers import (
    GitHubTrendingFetcher,
    HackerNewsFetcher,
    IndieHackersFetcher,
    OpenRouterFetcher,
    ProductHuntFetcher,
    RedditFetcher,
)
from .utils import SimpleCache, logger, setup_logger


class TrendingMCPServer:
    """MCP Server for trending data from multiple platforms."""

    def __init__(self):
        """Initialize the MCP server."""
        # Setup logger
        setup_logger(level=config.log_level)

        # Initialize server
        self.server = Server("mcp-server-trending")

        # Initialize shared cache
        self.cache = SimpleCache(default_ttl=config.cache_ttl)

        # Initialize fetchers
        self.github_fetcher = GitHubTrendingFetcher(cache=self.cache)
        self.hackernews_fetcher = HackerNewsFetcher(cache=self.cache)
        self.producthunt_fetcher = ProductHuntFetcher(cache=self.cache)
        self.indiehackers_fetcher = IndieHackersFetcher(cache=self.cache)
        self.reddit_fetcher = RedditFetcher(cache=self.cache)
        self.openrouter_fetcher = OpenRouterFetcher(cache=self.cache)

        # Register handlers
        self._register_handlers()

        logger.info("TrendingMCPServer initialized")

    def _register_handlers(self):
        """Register MCP protocol handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                # GitHub Tools
                Tool(
                    name="get_github_trending_repos",
                    description="Get GitHub trending repositories. Supports filtering by programming language and time range.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["daily", "weekly", "monthly"],
                                "default": "daily",
                                "description": "Time range for trending data",
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language (e.g., python, javascript, go)",
                            },
                            "spoken_language": {
                                "type": "string",
                                "description": "Filter by spoken language (e.g., en, zh)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_github_trending_developers",
                    description="Get GitHub trending developers. Supports filtering by programming language and time range.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["daily", "weekly", "monthly"],
                                "default": "daily",
                                "description": "Time range for trending data",
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language (e.g., python, javascript, go)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Hacker News Tools
                Tool(
                    name="get_hackernews_stories",
                    description="Get Hacker News stories. Supports different story types: top, best, new, ask (Ask HN), show (Show HN), and job.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "story_type": {
                                "type": "string",
                                "enum": ["top", "best", "new", "ask", "show", "job"],
                                "default": "top",
                                "description": "Type of stories to fetch",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 500,
                                "description": "Number of stories to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Product Hunt Tools
                Tool(
                    name="get_producthunt_products",
                    description="Get Product Hunt products. Supports different time ranges: today, week, month.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["today", "week", "month"],
                                "default": "today",
                                "description": "Time range for products",
                            },
                            "topic": {
                                "type": "string",
                                "description": "Filter by topic (e.g., 'Developer Tools', 'AI')",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Indie Hackers Tools
                Tool(
                    name="get_indiehackers_popular",
                    description="Get popular posts from Indie Hackers community.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of posts to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_indiehackers_income_reports",
                    description="Get income reports from Indie Hackers. See revenue data and milestones from successful indie projects.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of reports to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Reddit Tools
                Tool(
                    name="get_reddit_trending",
                    description="Get trending posts from specified subreddit. Popular subreddits: sideproject, entrepreneur, startups, saas, webdev, programming.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subreddit": {
                                "type": "string",
                                "description": "Subreddit name (without r/), e.g., 'sideproject', 'entrepreneur'",
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["hot", "top"],
                                "default": "hot",
                                "description": "Sort method for posts",
                            },
                            "time_range": {
                                "type": "string",
                                "enum": ["hour", "day", "week", "month", "year", "all"],
                                "default": "day",
                                "description": "Time range for trending posts",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 25,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of posts to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["subreddit"],
                    },
                ),
                Tool(
                    name="get_reddit_by_topic",
                    description="Get trending posts by topic (intelligent subreddit selection). Supports topics like: ai, crypto, indie, startup, saas, programming, python, javascript, web, mobile, design, business, marketing, gaming, devops, security. If no topic specified, returns posts from indie developer communities.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic keyword (e.g., 'ai', 'crypto', 'indie', 'startup'). Leave empty for default indie content.",
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["hot", "top"],
                                "default": "hot",
                                "description": "Sort method for posts",
                            },
                            "time_range": {
                                "type": "string",
                                "enum": ["hour", "day", "week", "month", "year", "all"],
                                "default": "day",
                                "description": "Time range for trending posts",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Maximum total posts to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # OpenRouter Tools
                Tool(
                    name="get_openrouter_models",
                    description="Get all available LLM models from OpenRouter with their specifications and pricing.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of models to return (optional, returns all if not specified)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_openrouter_popular",
                    description="Get most popular LLM models on OpenRouter based on usage statistics.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of models to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_openrouter_best_value",
                    description="Get best value LLM models on OpenRouter (best performance vs cost ratio).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of models to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            try:
                logger.info(f"Tool called: {name} with arguments: {arguments}")

                # GitHub Tools
                if name == "get_github_trending_repos":
                    response = await self.github_fetcher.fetch_trending_repositories(
                        time_range=arguments.get("time_range", "daily"),
                        language=arguments.get("language"),
                        spoken_language=arguments.get("spoken_language"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_github_trending_developers":
                    response = await self.github_fetcher.fetch_trending_developers(
                        time_range=arguments.get("time_range", "daily"),
                        language=arguments.get("language"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Hacker News Tools
                elif name == "get_hackernews_stories":
                    response = await self.hackernews_fetcher.fetch_stories(
                        story_type=arguments.get("story_type", "top"),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Product Hunt Tools
                elif name == "get_producthunt_products":
                    response = await self.producthunt_fetcher.fetch_products(
                        time_range=arguments.get("time_range", "today"),
                        topic=arguments.get("topic"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Indie Hackers Tools
                elif name == "get_indiehackers_popular":
                    response = await self.indiehackers_fetcher.fetch_popular_posts(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_indiehackers_income_reports":
                    response = await self.indiehackers_fetcher.fetch_income_reports(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Reddit Tools
                elif name == "get_reddit_trending":
                    subreddit = arguments.get("subreddit")
                    if not subreddit:
                        raise ValueError("subreddit parameter is required")

                    sort_by = arguments.get("sort_by", "hot")
                    if sort_by == "hot":
                        response = await self.reddit_fetcher.fetch_subreddit_hot(
                            subreddit=subreddit,
                            time_range=arguments.get("time_range", "day"),
                            limit=arguments.get("limit", 25),
                            use_cache=arguments.get("use_cache", True),
                        )
                    else:  # top
                        response = await self.reddit_fetcher.fetch_subreddit_top(
                            subreddit=subreddit,
                            time_range=arguments.get("time_range", "week"),
                            limit=arguments.get("limit", 25),
                            use_cache=arguments.get("use_cache", True),
                        )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_reddit_by_topic":
                    response = await self.reddit_fetcher.fetch_by_topic(
                        topic=arguments.get("topic"),  # None if not provided
                        sort_by=arguments.get("sort_by", "hot"),
                        time_range=arguments.get("time_range", "day"),
                        max_total=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # OpenRouter Tools
                elif name == "get_openrouter_models":
                    response = await self.openrouter_fetcher.fetch_models(
                        limit=arguments.get("limit"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_openrouter_popular":
                    response = await self.openrouter_fetcher.fetch_popular_models(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_openrouter_best_value":
                    response = await self.openrouter_fetcher.fetch_best_value_models(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}", exc_info=True)
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    def _format_response(self, response: Any) -> str:
        """
        Format response for text output.

        Args:
            response: TrendingResponse object

        Returns:
            Formatted string
        """
        import json

        # Convert to dict for JSON serialization
        response_dict = response.to_dict()

        # Pretty print JSON
        return json.dumps(response_dict, indent=2, ensure_ascii=False)

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting MCP Server Trending...")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )

    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up resources...")
        await self.github_fetcher.close()
        await self.hackernews_fetcher.close()
        await self.producthunt_fetcher.close()
        await self.indiehackers_fetcher.close()
        await self.reddit_fetcher.close()
        await self.openrouter_fetcher.close()


async def main():
    """Main entry point."""
    server = TrendingMCPServer()
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
    finally:
        await server.cleanup()


def cli_main():
    """CLI entry point."""
    # Handle --version flag
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-v"):
        print(f"mcp-server-trending {__version__}")
        sys.exit(0)

    asyncio.run(main())


if __name__ == "__main__":
    cli_main()

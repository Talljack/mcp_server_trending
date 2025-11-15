"""MCP Server implementation for Trending data."""

import asyncio
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from config import config
from fetchers import GitHubTrendingFetcher, HackerNewsFetcher, ProductHuntFetcher
from utils import SimpleCache, logger, setup_logger


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
                                "description": "Time range for trending data"
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language (e.g., python, javascript, go)"
                            },
                            "spoken_language": {
                                "type": "string",
                                "description": "Filter by spoken language (e.g., en, zh)"
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data"
                            }
                        }
                    }
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
                                "description": "Time range for trending data"
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language (e.g., python, javascript, go)"
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data"
                            }
                        }
                    }
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
                                "description": "Type of stories to fetch"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 500,
                                "description": "Number of stories to fetch"
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data"
                            }
                        }
                    }
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
                                "description": "Time range for products"
                            },
                            "topic": {
                                "type": "string",
                                "description": "Filter by topic (e.g., 'Developer Tools', 'AI')"
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data"
                            }
                        }
                    }
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
                    return [TextContent(
                        type="text",
                        text=self._format_response(response)
                    )]

                elif name == "get_github_trending_developers":
                    response = await self.github_fetcher.fetch_trending_developers(
                        time_range=arguments.get("time_range", "daily"),
                        language=arguments.get("language"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(
                        type="text",
                        text=self._format_response(response)
                    )]

                # Hacker News Tools
                elif name == "get_hackernews_stories":
                    response = await self.hackernews_fetcher.fetch_stories(
                        story_type=arguments.get("story_type", "top"),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(
                        type="text",
                        text=self._format_response(response)
                    )]

                # Product Hunt Tools
                elif name == "get_producthunt_products":
                    response = await self.producthunt_fetcher.fetch_products(
                        time_range=arguments.get("time_range", "today"),
                        topic=arguments.get("topic"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(
                        type="text",
                        text=self._format_response(response)
                    )]

                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

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
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up resources...")
        await self.github_fetcher.close()
        await self.hackernews_fetcher.close()
        await self.producthunt_fetcher.close()


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
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()

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
    AIToolsFetcher,
    DevToFetcher,
    GitHubTrendingFetcher,
    HackerNewsFetcher,
    HuggingFaceFetcher,
    IndieHackersFetcher,
    JuejinFetcher,
    ModelScopeFetcher,
    OpenRouterFetcher,
    ProductHuntFetcher,
    # RedditFetcher,  # Disabled: Requires Reddit API credentials
    TrustMRRFetcher,
    V2EXFetcher,
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
        # self.reddit_fetcher = RedditFetcher(cache=self.cache)  # Disabled: Requires credentials
        self.openrouter_fetcher = OpenRouterFetcher(cache=self.cache)
        self.trustmrr_fetcher = TrustMRRFetcher(cache=self.cache)
        self.aitools_fetcher = AIToolsFetcher(cache=self.cache)
        self.huggingface_fetcher = HuggingFaceFetcher(cache=self.cache)
        self.v2ex_fetcher = V2EXFetcher(cache=self.cache)
        self.juejin_fetcher = JuejinFetcher(cache=self.cache)
        self.devto_fetcher = DevToFetcher(cache=self.cache)
        self.modelscope_fetcher = ModelScopeFetcher(cache=self.cache)

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
                    description="Get income reports from Indie Hackers with Stripe-verified revenue. Filter by category (ai, saas, marketplace, ecommerce) and sort by revenue or trending.",
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
                            "category": {
                                "type": "string",
                                "description": "Filter by category: ai, saas, marketplace, ecommerce, content, community, etc.",
                            },
                            "sorting": {
                                "type": "string",
                                "enum": ["highest-revenue", "newest", "trending"],
                                "default": "highest-revenue",
                                "description": "Sort method for products",
                            },
                            "revenue_verification": {
                                "type": "string",
                                "enum": ["stripe", "all"],
                                "default": "stripe",
                                "description": "Filter by revenue verification (stripe for verified only)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Reddit Tools - Disabled: Requires Reddit API credentials
                # Tool(
                #     name="get_reddit_trending",
                #     description="Get trending posts from specified subreddit.",
                #     inputSchema={...},
                # ),
                # Tool(
                #     name="get_reddit_by_topic",
                #     description="Get trending posts by topic.",
                #     inputSchema={...},
                # ),
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
                # TrustMRR Tools
                Tool(
                    name="get_trustmrr_rankings",
                    description="Get MRR/revenue rankings from TrustMRR. See publicly shared revenue data from successful indie projects and SaaS products.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of projects to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # AI Tools Directory
                Tool(
                    name="get_ai_tools",
                    description="Get trending AI tools from directory (There's An AI For That). Discover the latest and most popular AI tools across different categories.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Filter by category (e.g., 'productivity', 'writing', 'design')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of tools to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # HuggingFace Tools
                Tool(
                    name="get_huggingface_models",
                    description="Get trending models from HuggingFace. Discover the most popular and downloaded ML models for various tasks like text generation, image classification, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "sort_by": {
                                "type": "string",
                                "enum": ["downloads", "likes", "modified"],
                                "default": "downloads",
                                "description": "Sort models by downloads, likes, or last modified",
                            },
                            "task": {
                                "type": "string",
                                "description": "Filter by task (e.g., 'text-generation', 'image-classification', 'text-to-image')",
                            },
                            "library": {
                                "type": "string",
                                "description": "Filter by library (e.g., 'transformers', 'diffusers', 'sentence-transformers')",
                            },
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
                    name="get_huggingface_datasets",
                    description="Get trending datasets from HuggingFace. Find popular datasets for training and fine-tuning ML models.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "sort_by": {
                                "type": "string",
                                "enum": ["downloads", "likes", "modified"],
                                "default": "downloads",
                                "description": "Sort datasets by downloads, likes, or last modified",
                            },
                            "task": {
                                "type": "string",
                                "description": "Filter by task category (e.g., 'text-classification', 'translation', 'question-answering')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of datasets to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # V2EX Tools
                Tool(
                    name="get_v2ex_hot_topics",
                    description="Get hot topics from V2EX Chinese community. Popular discussions across various tech and creative topics.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of topics to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Juejin (掘金) Tools
                Tool(
                    name="get_juejin_articles",
                    description="Get recommended articles from Juejin (掘金) Chinese tech community. Popular tech articles and tutorials.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of articles to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # dev.to Tools
                Tool(
                    name="get_devto_articles",
                    description="Get articles from dev.to English developer community. Supports filtering by tags and time periods.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "per_page": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of articles per page",
                            },
                            "tag": {
                                "type": "string",
                                "description": "Filter by tag (e.g., 'python', 'javascript', 'webdev')",
                            },
                            "top": {
                                "type": "integer",
                                "description": "Get top articles (1=daily, 7=weekly, 30=monthly, 365=yearly)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # ModelScope (魔塔社区) Tools
                Tool(
                    name="get_modelscope_models",
                    description="Get trending models from ModelScope (魔塔社区) Chinese AI model platform. Popular ML models from Chinese community.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_size": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of models per page",
                            },
                            "page_number": {
                                "type": "integer",
                                "default": 1,
                                "minimum": 1,
                                "description": "Page number",
                            },
                            "sort_by": {
                                "type": "string",
                                "default": "Default",
                                "description": "Sort by (Default, downloads, stars, etc.)",
                            },
                            "search_text": {
                                "type": "string",
                                "description": "Search text to filter models by name (e.g., 'GLM')",
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
                    name="get_modelscope_datasets",
                    description="Get trending datasets from ModelScope (魔塔社区) Chinese AI platform.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_size": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of datasets per page",
                            },
                            "page_number": {
                                "type": "integer",
                                "default": 1,
                                "minimum": 1,
                                "description": "Page number",
                            },
                            "target": {
                                "type": "string",
                                "default": "",
                                "description": "Target filter (optional)",
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
                        category=arguments.get("category"),
                        sorting=arguments.get("sorting", "highest-revenue"),
                        revenue_verification=arguments.get("revenue_verification", "stripe"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Reddit Tools - Disabled: Requires Reddit API credentials
                # elif name == "get_reddit_trending":
                #     subreddit = arguments.get("subreddit")
                #     if not subreddit:
                #         raise ValueError("subreddit parameter is required")
                #
                #     sort_by = arguments.get("sort_by", "hot")
                #     if sort_by == "hot":
                #         response = await self.reddit_fetcher.fetch_subreddit_hot(
                #             subreddit=subreddit,
                #             time_range=arguments.get("time_range", "day"),
                #             limit=arguments.get("limit", 25),
                #             use_cache=arguments.get("use_cache", True),
                #         )
                #     else:  # top
                #         response = await self.reddit_fetcher.fetch_subreddit_top(
                #             subreddit=subreddit,
                #             time_range=arguments.get("time_range", "week"),
                #             limit=arguments.get("limit", 25),
                #             use_cache=arguments.get("use_cache", True),
                #         )
                #     return [TextContent(type="text", text=self._format_response(response))]
                #
                # elif name == "get_reddit_by_topic":
                #     response = await self.reddit_fetcher.fetch_by_topic(
                #         topic=arguments.get("topic"),  # None if not provided
                #         sort_by=arguments.get("sort_by", "hot"),
                #         time_range=arguments.get("time_range", "day"),
                #         max_total=arguments.get("limit", 50),
                #         use_cache=arguments.get("use_cache", True),
                #     )
                #     return [TextContent(type="text", text=self._format_response(response))]

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

                # TrustMRR Tools
                elif name == "get_trustmrr_rankings":
                    response = await self.trustmrr_fetcher.fetch_rankings(
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # AI Tools Directory
                elif name == "get_ai_tools":
                    response = await self.aitools_fetcher.fetch_trending(
                        category=arguments.get("category"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # HuggingFace Tools
                elif name == "get_huggingface_models":
                    response = await self.huggingface_fetcher.fetch_trending_models(
                        sort_by=arguments.get("sort_by", "downloads"),
                        task=arguments.get("task"),
                        library=arguments.get("library"),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_huggingface_datasets":
                    response = await self.huggingface_fetcher.fetch_trending_datasets(
                        sort_by=arguments.get("sort_by", "downloads"),
                        task=arguments.get("task"),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # V2EX Tools
                elif name == "get_v2ex_hot_topics":
                    response = await self.v2ex_fetcher.fetch_hot_topics(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Juejin Tools
                elif name == "get_juejin_articles":
                    response = await self.juejin_fetcher.fetch_recommended_articles(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # dev.to Tools
                elif name == "get_devto_articles":
                    response = await self.devto_fetcher.fetch_articles(
                        per_page=arguments.get("per_page", 30),
                        tag=arguments.get("tag"),
                        top=arguments.get("top"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # ModelScope Tools
                elif name == "get_modelscope_models":
                    response = await self.modelscope_fetcher.fetch_models(
                        page_number=arguments.get("page_number", 1),
                        page_size=arguments.get("page_size", 20),
                        sort_by=arguments.get("sort_by", "Default"),
                        search_text=arguments.get("search_text"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_modelscope_datasets":
                    response = await self.modelscope_fetcher.fetch_datasets(
                        page_number=arguments.get("page_number", 1),
                        page_size=arguments.get("page_size", 20),
                        target=arguments.get("target", ""),
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
        # await self.reddit_fetcher.close()  # Disabled: Requires Reddit API credentials
        await self.openrouter_fetcher.close()
        await self.trustmrr_fetcher.close()
        await self.aitools_fetcher.close()
        await self.huggingface_fetcher.close()
        await self.v2ex_fetcher.close()
        await self.juejin_fetcher.close()
        await self.devto_fetcher.close()
        await self.modelscope_fetcher.close()


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

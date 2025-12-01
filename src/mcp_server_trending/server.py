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
    AggregationFetcher,
    AIToolsFetcher,
    AlternativeToFetcher,
    ArxivFetcher,
    AwesomeFetcher,
    BetalistFetcher,
    ChromeWebStoreFetcher,
    CodePenFetcher,
    DevToFetcher,
    EchoJSFetcher,
    GitHubTrendingFetcher,
    GumroadFetcher,
    HackerNewsFetcher,
    HashnodeFetcher,
    HuggingFaceFetcher,
    IndieHackersFetcher,
    JuejinFetcher,
    LobstersFetcher,
    MediumFetcher,
    ModelScopeFetcher,
    NPMFetcher,
    OpenReviewFetcher,
    OpenRouterFetcher,
    PapersWithCodeFetcher,
    ProductHuntFetcher,
    PyPIFetcher,
    # RedditFetcher,  # Disabled: Requires Reddit API credentials
    RemoteOKFetcher,
    ReplicateFetcher,
    SemanticScholarFetcher,
    StackOverflowFetcher,
    TrustMRRFetcher,
    TwitterFetcher,
    V2EXFetcher,
    VSCodeMarketplaceFetcher,
    WeWorkRemotelyFetcher,
    WordPressFetcher,
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
        self.stackoverflow_fetcher = StackOverflowFetcher(cache=self.cache)
        self.awesome_fetcher = AwesomeFetcher(cache=self.cache)
        self.vscode_fetcher = VSCodeMarketplaceFetcher(cache=self.cache)
        self.npm_fetcher = NPMFetcher(cache=self.cache)
        self.chrome_fetcher = ChromeWebStoreFetcher(cache=self.cache)
        self.pypi_fetcher = PyPIFetcher(cache=self.cache)
        self.remoteok_fetcher = RemoteOKFetcher(cache=self.cache)
        self.wordpress_fetcher = WordPressFetcher(cache=self.cache)

        # New fetchers for Hashnode, CodePen, Medium
        self.hashnode_fetcher = HashnodeFetcher(cache=self.cache)
        self.codepen_fetcher = CodePenFetcher(cache=self.cache)
        self.medium_fetcher = MediumFetcher(cache=self.cache)

        # New fetchers for Lobsters, Echo JS, We Work Remotely
        self.lobsters_fetcher = LobstersFetcher(cache=self.cache)
        self.echojs_fetcher = EchoJSFetcher(cache=self.cache)
        self.weworkremotely_fetcher = WeWorkRemotelyFetcher(cache=self.cache)

        # New fetchers for Papers with Code, AlternativeTo, Replicate, Betalist
        self.paperswithcode_fetcher = PapersWithCodeFetcher(cache=self.cache)
        self.alternativeto_fetcher = AlternativeToFetcher(cache=self.cache)
        self.replicate_fetcher = ReplicateFetcher(cache=self.cache)
        self.betalist_fetcher = BetalistFetcher(cache=self.cache)

        # Twitter/X fetcher (via Nitter)
        self.twitter_fetcher = TwitterFetcher(cache=self.cache)

        # Gumroad fetcher
        self.gumroad_fetcher = GumroadFetcher(cache=self.cache)

        # Research paper fetchers with longer cache TTL (papers update slowly)
        # All paper platforms: 24 hours cache - papers and citations update slowly
        paper_cache_ttl = 86400  # 24 hours
        self.arxiv_fetcher = ArxivFetcher(cache=self.cache, cache_ttl=paper_cache_ttl)
        self.semanticscholar_fetcher = SemanticScholarFetcher(
            cache=self.cache, cache_ttl=paper_cache_ttl, api_key=config.semanticscholar_api_key
        )
        self.openreview_fetcher = OpenReviewFetcher(cache=self.cache, cache_ttl=paper_cache_ttl)

        # Initialize aggregation fetcher with references to other fetchers
        self.aggregation_fetcher = AggregationFetcher(
            cache=self.cache,
            github=self.github_fetcher,
            npm=self.npm_fetcher,
            pypi=self.pypi_fetcher,
            stackoverflow=self.stackoverflow_fetcher,
            vscode=self.vscode_fetcher,
            remoteok=self.remoteok_fetcher,
            indiehackers=self.indiehackers_fetcher,
            trustmrr=self.trustmrr_fetcher,
            hackernews=self.hackernews_fetcher,
            devto=self.devto_fetcher,
            juejin=self.juejin_fetcher,
        )

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
                    description="Get GitHub trending repositories. Supports filtering by programming language and time range. Use this when user asks about popular/trending/hot repos on GitHub.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["daily", "weekly", "monthly"],
                                "default": "daily",
                                "description": "Time range for trending data. Use 'daily' for today/24h, 'weekly' for this week/7 days/past week, 'monthly' for this month/30 days/past month. Default is daily.",
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language filter. Examples: 'python', 'javascript', 'typescript', 'go', 'rust', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin'. Leave empty for all languages.",
                            },
                            "spoken_language": {
                                "type": "string",
                                "description": "Spoken/natural language filter. Examples: 'en' for English, 'zh' for Chinese, 'ja' for Japanese, 'ko' for Korean, 'es' for Spanish. Leave empty for all.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data. Set to false for real-time fresh data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_github_trending_developers",
                    description="Get GitHub trending developers/contributors. Use this when user asks about popular developers, top contributors, or influential programmers on GitHub.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["daily", "weekly", "monthly"],
                                "default": "daily",
                                "description": "Time range for trending data. Use 'daily' for today/24h, 'weekly' for this week/7 days, 'monthly' for this month/30 days.",
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language filter. Examples: 'python', 'javascript', 'rust', 'go'. Leave empty for all languages.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                # Hacker News Tools
                Tool(
                    name="get_hackernews_stories",
                    description="Get Hacker News stories. Use this for tech news, startup discussions, programming articles. Supports different story types.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "story_type": {
                                "type": "string",
                                "enum": ["top", "best", "new", "ask", "show", "job"],
                                "default": "top",
                                "description": "Type of stories: 'top' for front page/trending, 'best' for highest voted/all-time best, 'new' for latest/newest/recent, 'ask' for Ask HN questions/discussions, 'show' for Show HN project demos/launches, 'job' for job postings/hiring.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 500,
                                "description": "Number of stories to fetch. Use 10-30 for quick overview, 50-100 for comprehensive list.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                # Product Hunt Tools
                Tool(
                    name="get_producthunt_products",
                    description="Get Product Hunt products. Use this for new product launches, startup products, tech tools. Great for discovering new apps and services.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["today", "week", "month"],
                                "default": "today",
                                "description": "Time range: 'today' for today's launches/daily, 'week' for this week's top products/weekly best, 'month' for this month's top products/monthly best.",
                            },
                            "topic": {
                                "type": "string",
                                "description": "Filter by topic/category. Examples: 'Developer Tools', 'AI', 'Productivity', 'Design Tools', 'Marketing', 'SaaS', 'Mobile Apps', 'Chrome Extensions'. Leave empty for all topics.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
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
                # Hashnode Tools
                Tool(
                    name="get_hashnode_trending_articles",
                    description="Get trending articles from Hashnode developer blogging platform. View popular technical blog posts from the Hashnode community.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of articles to fetch",
                            },
                            "tag": {
                                "type": "string",
                                "description": "Filter by tag slug (e.g., 'javascript', 'python', 'ai')",
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["popular", "recent", "featured"],
                                "default": "popular",
                                "description": "Sort order",
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
                    name="get_hashnode_publication_articles",
                    description="Get articles from a specific Hashnode publication. Follow popular tech publications on Hashnode.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "publication_host": {
                                "type": "string",
                                "description": "Publication hostname (e.g., 'engineering.hashnode.com', 'blog.hashnode.com')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of articles to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["publication_host"],
                    },
                ),
                # CodePen Tools
                Tool(
                    name="get_codepen_popular_pens",
                    description="Get popular code snippets from CodePen. Discover trending front-end code examples and inspiration.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "integer",
                                "default": 1,
                                "minimum": 1,
                                "description": "Page number",
                            },
                            "tag": {
                                "type": "string",
                                "description": "Filter by tag (e.g., 'animation', '3d', 'canvas')",
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
                    name="get_codepen_picked_pens",
                    description="Get featured/picked pens from CodePen. View hand-selected high-quality front-end examples.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "integer",
                                "default": 1,
                                "minimum": 1,
                                "description": "Page number",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Medium Tools
                Tool(
                    name="get_medium_tag_articles",
                    description="Get articles from a Medium tag. Discover popular technical writing on Medium by topic.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag": {
                                "type": "string",
                                "description": "Tag name (e.g., 'programming', 'ai', 'blockchain', 'data-science')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of articles to fetch",
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["latest", "top"],
                                "default": "latest",
                                "description": "Sort mode",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["tag"],
                    },
                ),
                Tool(
                    name="get_medium_publication_articles",
                    description="Get articles from a Medium publication. Follow popular tech publications like Towards Data Science, HackerNoon, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "publication": {
                                "type": "string",
                                "description": "Publication slug (e.g., 'hackernoon', 'towardsdatascience', 'better-programming')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of articles to fetch",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["publication"],
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
                # Stack Overflow Tools
                Tool(
                    name="get_stackoverflow_trends",
                    description="Get Stack Overflow trending tags. Shows popular technology tags with question counts and activity.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "sort": {
                                "type": "string",
                                "enum": ["popular", "activity", "name"],
                                "default": "popular",
                                "description": "Sort order: popular (by question count), activity (by last activity), name (alphabetical)",
                            },
                            "order": {
                                "type": "string",
                                "enum": ["desc", "asc"],
                                "default": "desc",
                                "description": "Sort direction",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of tags to fetch",
                            },
                            "site": {
                                "type": "string",
                                "default": "stackoverflow",
                                "description": "Stack Exchange site (default: stackoverflow)",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Awesome Lists Tools
                Tool(
                    name="get_awesome_lists",
                    description="Get Awesome Lists from GitHub. Curated lists of awesome resources organized by topic.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "sort": {
                                "type": "string",
                                "enum": ["stars", "forks", "updated"],
                                "default": "stars",
                                "description": "Sort order: stars, forks, or updated",
                            },
                            "order": {
                                "type": "string",
                                "enum": ["desc", "asc"],
                                "default": "desc",
                                "description": "Sort direction",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of awesome lists to fetch",
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language (e.g., 'python', 'javascript')",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # VS Code Extensions Tools
                Tool(
                    name="get_vscode_extensions",
                    description="Get trending VS Code extensions from Visual Studio Marketplace. Discover popular extensions for development, themes, productivity, and more.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "sort_by": {
                                "type": "string",
                                "enum": ["installs", "rating", "trending", "updated"],
                                "default": "installs",
                                "description": "Sort by (installs, rating, trending, updated)",
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category (e.g., 'Programming Languages', 'Themes', 'Debuggers')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of extensions to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # npm Packages Tools
                Tool(
                    name="get_npm_packages",
                    description="Get trending npm packages. Discover popular JavaScript/Node.js packages by category or keyword.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["week", "month"],
                                "default": "week",
                                "description": "Time range for trending data",
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by keyword/category (e.g., 'react', 'vue', 'ai', 'cli')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 250,
                                "description": "Number of packages to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Chrome Extensions Tools
                Tool(
                    name="get_chrome_extensions",
                    description="Get popular Chrome Web Store extensions. Note: Chrome Web Store doesn't have a public API, so this returns curated data for known popular extensions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "default": "productivity",
                                "description": "Extension category (productivity, developer-tools, etc.)",
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["popular", "rating", "featured"],
                                "default": "popular",
                                "description": "Sort method",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of extensions to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # PyPI Packages Tools
                Tool(
                    name="get_pypi_packages",
                    description="Get trending PyPI packages. Discover popular Python packages by category or keyword.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Filter by keyword/category (e.g., 'django', 'machine-learning', 'data')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 250,
                                "description": "Number of packages to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # RemoteOK Jobs Tools
                Tool(
                    name="get_remote_jobs",
                    description="Get remote job listings from RemoteOK. Filter by tags and search keywords.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags (e.g., ['python', 'remote', 'full-time'])",
                            },
                            "search": {
                                "type": "string",
                                "description": "Search keyword (e.g., 'senior developer', 'machine learning')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 200,
                                "description": "Number of jobs to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # WordPress Plugins Tools
                Tool(
                    name="get_wordpress_plugins",
                    description="Get trending WordPress plugins from the official WordPress.org directory. Discover popular, new, featured, or updated plugins.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "browse": {
                                "type": "string",
                                "enum": ["popular", "featured", "new", "updated"],
                                "default": "popular",
                                "description": "Browse type",
                            },
                            "search": {
                                "type": "string",
                                "description": "Search keyword (e.g., 'seo', 'ecommerce', 'security')",
                            },
                            "tag": {
                                "type": "string",
                                "description": "Filter by tag (e.g., 'security', 'performance', 'seo')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of plugins to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Research Paper Tools
                Tool(
                    name="get_arxiv_papers",
                    description="Get research papers from arXiv.org preprint repository. Search by category (cs.AI, cs.LG, cs.CV, etc.) or keywords. Covers Computer Science, Math, Physics, and more.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "arXiv category (e.g., 'cs.AI', 'cs.LG', 'cs.CV', 'cs.CL', 'stat.ML')",
                            },
                            "search_query": {
                                "type": "string",
                                "description": "Search keywords (e.g., 'transformers', 'neural networks')",
                            },
                            "sort_by": {
                                "type": "string",
                                "enum": ["submittedDate", "lastUpdatedDate", "relevance"],
                                "default": "submittedDate",
                                "description": "Sort field",
                            },
                            "sort_order": {
                                "type": "string",
                                "enum": ["descending", "ascending"],
                                "default": "descending",
                                "description": "Sort order",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 2000,
                                "description": "Number of papers to return",
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
                    name="search_semantic_scholar",
                    description="Search academic papers on Semantic Scholar with AI-powered relevance and citation metrics. Get influential citations, open access PDFs, and comprehensive author information.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (e.g., 'transformers', 'neural networks', 'deep learning')",
                            },
                            "fields_of_study": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by fields (e.g., ['Computer Science', 'Medicine'])",
                            },
                            "year": {
                                "type": "string",
                                "description": "Year range (e.g., '2020-2023', '2023')",
                            },
                            "min_citation_count": {
                                "type": "integer",
                                "description": "Minimum citation count",
                            },
                            "open_access_pdf": {
                                "type": "boolean",
                                "default": False,
                                "description": "Only papers with open access PDFs",
                            },
                            "sort": {
                                "type": "string",
                                "enum": ["citationCount:desc", "publicationDate:desc", "relevance"],
                                "default": "citationCount:desc",
                                "description": "Sort order",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 100,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of papers to return",
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
                    name="get_openreview_papers",
                    description="Get papers from OpenReview ML conferences (ICLR, NeurIPS, ICML). Access peer review scores, decisions, and ratings from top ML conferences.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "venue": {
                                "type": "string",
                                "default": "ICLR.cc/2024/Conference",
                                "description": "Venue (e.g., 'ICLR.cc/2024/Conference', 'iclr2024', 'neurips2023')",
                            },
                            "content": {
                                "type": "string",
                                "description": "Search in title/abstract",
                            },
                            "decision": {
                                "type": "string",
                                "description": "Filter by decision (e.g., 'Accept', 'Reject')",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 100,
                                "minimum": 1,
                                "maximum": 1000,
                                "description": "Number of papers to return",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                # Aggregation Analysis Tools
                Tool(
                    name="analyze_tech_stack",
                    description="Analyze technology stack popularity across multiple platforms (GitHub, npm, PyPI, Stack Overflow, VS Code, job postings). Get a comprehensive view of a technology's ecosystem.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tech": {
                                "type": "string",
                                "description": "Technology name (e.g., 'nextjs', 'python', 'react', 'vue')",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["tech"],
                    },
                ),
                Tool(
                    name="get_indie_revenue_dashboard",
                    description="Get aggregated indie developer revenue dashboard from Indie Hackers and TrustMRR. View revenue statistics, top categories, and success stories.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                    },
                ),
                Tool(
                    name="track_topic_trends",
                    description="Track topic trends across multiple platforms (Hacker News, GitHub, Stack Overflow, dev.to, Juejin). Discover emerging topics and technologies.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to track (e.g., 'ai-agents', 'web3', 'serverless', 'edge-computing')",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data",
                            },
                        },
                        "required": ["topic"],
                    },
                ),
                # Lobsters Tools
                Tool(
                    name="get_lobsters_hottest",
                    description="Get hottest/trending stories from Lobsters. A computing-focused community with high-quality technical content, similar to Hacker News but more focused on programming and systems.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 25,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of stories to fetch. Use 10-25 for quick overview.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_lobsters_newest",
                    description="Get newest/latest stories from Lobsters. Fresh technical content from the computing community.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 25,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of stories to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_lobsters_by_tag",
                    description="Get Lobsters stories filtered by programming language or topic tag.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag": {
                                "type": "string",
                                "description": "Tag to filter. Examples: 'python', 'javascript', 'rust', 'go', 'c', 'java', 'ai', 'ml', 'security', 'linux', 'databases', 'devops', 'web', 'networking', 'programming', 'plt' (programming language theory).",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 25,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of stories to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["tag"],
                    },
                ),
                # Echo JS Tools
                Tool(
                    name="get_echojs_latest",
                    description="Get latest JavaScript/front-end news from Echo JS. Use this for JS news, React, Vue, Angular, Node.js, TypeScript, HTML5, CSS news and tutorials.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of news items to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_echojs_top",
                    description="Get top/trending/popular JavaScript news from Echo JS. Most upvoted JavaScript and front-end content.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of news items to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                # We Work Remotely Tools
                Tool(
                    name="get_weworkremotely_jobs",
                    description="Get remote job listings from We Work Remotely. Use this for remote work opportunities, work from home jobs, distributed team positions in tech.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": [
                                    "programming",
                                    "design",
                                    "devops",
                                    "management",
                                    "sales",
                                    "customer-support",
                                    "finance",
                                    "product",
                                    "all",
                                ],
                                "default": "programming",
                                "description": "Job category: 'programming' for software/web/mobile dev, 'design' for UI/UX/graphic design, 'devops' for DevOps/SRE/infrastructure, 'management' for project/product managers, 'sales' for sales/business dev, 'customer-support' for support roles, 'finance' for finance/accounting, 'product' for product roles, 'all' for all categories.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of jobs to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                # Papers with Code Tools (via HuggingFace Daily Papers)
                Tool(
                    name="get_paperswithcode_trending",
                    description="Get trending ML/AI research papers with code. Use this for latest AI research, machine learning papers, deep learning advances. Data from HuggingFace Daily Papers.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of papers to fetch. Use 10-20 for quick overview, 50+ for comprehensive research.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_paperswithcode_latest",
                    description="Get latest ML/AI research papers. Most recently published papers with code implementations.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of papers to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="search_paperswithcode",
                    description="Search ML/AI research papers by keyword. Find papers on specific topics like transformers, diffusion models, LLMs, computer vision, NLP.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search keyword. Examples: 'transformer', 'diffusion', 'llm', 'large language model', 'gpt', 'vision', 'multimodal', 'reinforcement learning', 'neural network', 'attention mechanism'.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of papers to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                # AlternativeTo Tools
                Tool(
                    name="get_alternativeto_trending",
                    description="Get trending/popular software alternatives. Use this to discover popular apps, open-source alternatives, free software options across different platforms.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "platform": {
                                "type": "string",
                                "enum": [
                                    "all",
                                    "windows",
                                    "mac",
                                    "linux",
                                    "android",
                                    "iphone",
                                    "web",
                                ],
                                "default": "all",
                                "description": "Platform filter: 'all' for cross-platform, 'windows' for Windows apps, 'mac' for macOS apps, 'linux' for Linux apps, 'android' for Android apps, 'iphone' for iOS apps, 'web' for web-based apps/SaaS.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of apps to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="search_alternativeto",
                    description="Find alternatives to specific software. Use this when user asks 'what can I use instead of X' or 'alternatives to X' or 'free version of X'.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Software name to find alternatives for. Examples: 'photoshop' (image editing), 'slack' (team chat), 'notion' (notes), 'figma' (design), 'vscode' (code editor), 'zoom' (video calls), 'trello' (project management).",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of alternatives to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                # Replicate Tools
                Tool(
                    name="get_replicate_trending",
                    description="Get trending AI models from Replicate. Use this for popular ML models that can be run via API - image generation, LLMs, audio, video models.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of models to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_replicate_collection",
                    description="Get AI models from a specific Replicate collection. Use this when user asks about specific types of AI models.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection": {
                                "type": "string",
                                "enum": [
                                    "text-to-image",
                                    "image-to-image",
                                    "language-models",
                                    "audio",
                                    "video",
                                    "3d",
                                    "upscalers",
                                ],
                                "default": "text-to-image",
                                "description": "Model collection: 'text-to-image' for image generation/AI art (Stable Diffusion, DALL-E, Midjourney style), 'image-to-image' for image editing/transformation, 'language-models' for LLMs/text generation/chatbots, 'audio' for speech/music/voice models, 'video' for video generation/editing, '3d' for 3D model generation, 'upscalers' for image upscaling/enhancement.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of models to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                # Betalist Tools
                Tool(
                    name="get_betalist_featured",
                    description="Get featured startups from Betalist. Use this for discovering new startups, early-stage products, beta launches, indie projects.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of startups to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_betalist_latest",
                    description="Get latest/newest startups from Betalist. Most recently submitted startups and beta products.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of startups to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_betalist_by_topic",
                    description="Get startups by topic/category from Betalist. Filter startups by industry or type.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic/category to filter. Examples: 'ai' for AI/ML startups, 'saas' for SaaS products, 'fintech' for financial tech, 'productivity' for productivity tools, 'developer-tools' for dev tools, 'marketing' for marketing tools, 'ecommerce' for e-commerce, 'health' for healthcare/wellness.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Number of startups to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["topic"],
                    },
                ),
                # Twitter/X Tools (via Nitter)
                Tool(
                    name="get_twitter_hashtag_tweets",
                    description="Get tweets by hashtag from Twitter/X. Use this to find tweets about specific topics like #buildinpublic, #indiehackers, #saas, #startup, #webdev, #ai, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "hashtag": {
                                "type": "string",
                                "description": "Hashtag to search (without #). Examples: 'buildinpublic', 'indiehackers', 'saas', 'startup', 'webdev', 'javascript', 'python', 'ai', 'opensource'.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of tweets to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["hashtag"],
                    },
                ),
                Tool(
                    name="get_twitter_user_tweets",
                    description="Get tweets from a specific Twitter/X user. Use this to see what a specific person is tweeting about.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username (without @). Examples: 'levelsio', 'elonmusk', 'naval'.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of tweets to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["username"],
                    },
                ),
                Tool(
                    name="get_twitter_tech_tweets",
                    description="Get trending tech tweets aggregated from popular hashtags (#buildinpublic, #indiehackers, #saas, #startup, #webdev). Use this for a quick overview of what's trending in tech Twitter.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Total number of tweets to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_twitter_indie_hackers",
                    description="Get tweets from popular indie hackers and tech influencers (levelsio, marc_louvion, dannypostmaa, taborsky_, etc.). Use this to see what successful indie hackers are sharing.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of tweets to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_twitter_user_profile",
                    description="Get a Twitter/X user's profile information including bio, follower count, and stats.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username (without @).",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["username"],
                    },
                ),
                # Gumroad Tools
                Tool(
                    name="get_gumroad_discover",
                    description="Get trending/featured products from Gumroad discover page. Use this to find popular digital products being sold by creators.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": [
                                    "programming",
                                    "design",
                                    "software",
                                    "business",
                                    "education",
                                    "writing",
                                    "music",
                                    "films",
                                    "games",
                                    "3d",
                                    "audio",
                                    "photography",
                                    "fitness-and-health",
                                    "self-improvement",
                                ],
                                "description": "Product category to filter. Leave empty for all categories.",
                            },
                            "sort": {
                                "type": "string",
                                "enum": ["featured", "newest", "popular"],
                                "default": "featured",
                                "description": "Sort order: 'featured' for curated picks, 'newest' for latest, 'popular' for most popular.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of products to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_gumroad_programming",
                    description="Get programming-related products from Gumroad (code, tutorials, courses, ebooks). Perfect for developers looking for resources.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of products to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="get_gumroad_design",
                    description="Get design-related products from Gumroad (templates, assets, UI kits, courses). Great for designers and product makers.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of products to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                    },
                ),
                Tool(
                    name="search_gumroad",
                    description="Search for products on Gumroad by keyword. Find specific types of digital products.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query. Examples: 'notion templates', 'figma ui kit', 'python course', 'startup guide'.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of products to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="get_gumroad_creator",
                    description="Get products from a specific Gumroad creator. See what a creator is selling.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Creator's Gumroad username.",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50,
                                "description": "Number of products to fetch.",
                            },
                            "use_cache": {
                                "type": "boolean",
                                "default": True,
                                "description": "Whether to use cached data.",
                            },
                        },
                        "required": ["username"],
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

                # Hashnode Tools
                elif name == "get_hashnode_trending_articles":
                    response = await self.hashnode_fetcher.fetch_trending_articles(
                        limit=arguments.get("limit", 20),
                        tag=arguments.get("tag"),
                        sort_by=arguments.get("sort_by", "popular"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_hashnode_publication_articles":
                    publication_host = arguments.get("publication_host")
                    if not publication_host:
                        raise ValueError("publication_host parameter is required")
                    response = await self.hashnode_fetcher.fetch_publication_articles(
                        publication_host=publication_host,
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # CodePen Tools
                elif name == "get_codepen_popular_pens":
                    response = await self.codepen_fetcher.fetch_popular_pens(
                        page=arguments.get("page", 1),
                        tag=arguments.get("tag"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_codepen_picked_pens":
                    response = await self.codepen_fetcher.fetch_picked_pens(
                        page=arguments.get("page", 1),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Medium Tools
                elif name == "get_medium_tag_articles":
                    tag = arguments.get("tag")
                    if not tag:
                        raise ValueError("tag parameter is required")
                    response = await self.medium_fetcher.fetch_tag_articles(
                        tag=tag,
                        limit=arguments.get("limit", 20),
                        mode=arguments.get("mode", "latest"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_medium_publication_articles":
                    publication = arguments.get("publication")
                    if not publication:
                        raise ValueError("publication parameter is required")
                    response = await self.medium_fetcher.fetch_publication_articles(
                        publication=publication,
                        limit=arguments.get("limit", 20),
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

                # Stack Overflow Tools
                elif name == "get_stackoverflow_trends":
                    response = await self.stackoverflow_fetcher.fetch_tags(
                        sort=arguments.get("sort", "popular"),
                        order=arguments.get("order", "desc"),
                        limit=arguments.get("limit", 30),
                        site=arguments.get("site", "stackoverflow"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Awesome Lists Tools
                elif name == "get_awesome_lists":
                    response = await self.awesome_fetcher.fetch_awesome_lists(
                        sort=arguments.get("sort", "stars"),
                        order=arguments.get("order", "desc"),
                        limit=arguments.get("limit", 30),
                        language=arguments.get("language"),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # VS Code Extensions Tools
                elif name == "get_vscode_extensions":
                    response = await self.vscode_fetcher.fetch_trending_extensions(
                        sort_by=arguments.get("sort_by", "installs"),
                        category=arguments.get("category"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # npm Packages Tools
                elif name == "get_npm_packages":
                    response = await self.npm_fetcher.fetch_trending_packages(
                        time_range=arguments.get("time_range", "week"),
                        category=arguments.get("category"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Chrome Extensions Tools
                elif name == "get_chrome_extensions":
                    response = await self.chrome_fetcher.fetch_trending_extensions(
                        category=arguments.get("category", "productivity"),
                        sort_by=arguments.get("sort_by", "popular"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # PyPI Packages Tools
                elif name == "get_pypi_packages":
                    response = await self.pypi_fetcher.fetch_trending_packages(
                        category=arguments.get("category"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # RemoteOK Jobs Tools
                elif name == "get_remote_jobs":
                    response = await self.remoteok_fetcher.fetch_jobs(
                        tags=arguments.get("tags"),
                        search=arguments.get("search"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # WordPress Plugins Tools
                elif name == "get_wordpress_plugins":
                    response = await self.wordpress_fetcher.fetch_plugins(
                        browse=arguments.get("browse", "popular"),
                        search=arguments.get("search"),
                        tag=arguments.get("tag"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Research Paper Tools
                elif name == "get_arxiv_papers":
                    response = await self.arxiv_fetcher.fetch_papers(
                        category=arguments.get("category"),
                        search_query=arguments.get("search_query"),
                        sort_by=arguments.get("sort_by", "submittedDate"),
                        sort_order=arguments.get("sort_order", "descending"),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "search_semantic_scholar":
                    response = await self.semanticscholar_fetcher.search_papers(
                        query=arguments.get("query"),
                        fields_of_study=arguments.get("fields_of_study"),
                        year=arguments.get("year"),
                        min_citation_count=arguments.get("min_citation_count"),
                        open_access_pdf=arguments.get("open_access_pdf", False),
                        sort=arguments.get("sort", "citationCount:desc"),
                        limit=arguments.get("limit", 100),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_openreview_papers":
                    response = await self.openreview_fetcher.fetch_papers(
                        venue=arguments.get("venue", "ICLR.cc/2024/Conference"),
                        content=arguments.get("content"),
                        decision=arguments.get("decision"),
                        limit=arguments.get("limit", 100),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Aggregation Analysis Tools
                elif name == "analyze_tech_stack":
                    tech = arguments.get("tech")
                    if not tech:
                        raise ValueError("tech parameter is required")

                    response = await self.aggregation_fetcher.analyze_tech_stack(
                        tech=tech,
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_indie_revenue_dashboard":
                    response = await self.aggregation_fetcher.get_indie_revenue_dashboard(
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "track_topic_trends":
                    topic = arguments.get("topic")
                    if not topic:
                        raise ValueError("topic parameter is required")

                    response = await self.aggregation_fetcher.track_topic_trends(
                        topic=topic,
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Lobsters Tools
                elif name == "get_lobsters_hottest":
                    response = await self.lobsters_fetcher.fetch_hottest(
                        limit=arguments.get("limit", 25),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_lobsters_newest":
                    response = await self.lobsters_fetcher.fetch_newest(
                        limit=arguments.get("limit", 25),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_lobsters_by_tag":
                    tag = arguments.get("tag")
                    if not tag:
                        raise ValueError("tag parameter is required")
                    response = await self.lobsters_fetcher.fetch_by_tag(
                        tag=tag,
                        limit=arguments.get("limit", 25),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Echo JS Tools
                elif name == "get_echojs_latest":
                    response = await self.echojs_fetcher.fetch_latest(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_echojs_top":
                    response = await self.echojs_fetcher.fetch_top(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # We Work Remotely Tools
                elif name == "get_weworkremotely_jobs":
                    response = await self.weworkremotely_fetcher.fetch_jobs(
                        category=arguments.get("category", "programming"),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Papers with Code Tools
                elif name == "get_paperswithcode_trending":
                    response = await self.paperswithcode_fetcher.fetch_trending_papers(
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_paperswithcode_latest":
                    response = await self.paperswithcode_fetcher.fetch_latest_papers(
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "search_paperswithcode":
                    response = await self.paperswithcode_fetcher.search_papers(
                        query=arguments.get("query", ""),
                        limit=arguments.get("limit", 50),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # AlternativeTo Tools
                elif name == "get_alternativeto_trending":
                    response = await self.alternativeto_fetcher.fetch_trending(
                        platform=arguments.get("platform", "all"),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "search_alternativeto":
                    response = await self.alternativeto_fetcher.search_alternatives(
                        query=arguments.get("query", ""),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Replicate Tools
                elif name == "get_replicate_trending":
                    response = await self.replicate_fetcher.fetch_trending_models(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_replicate_collection":
                    response = await self.replicate_fetcher.fetch_collection(
                        collection=arguments.get("collection", "text-to-image"),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Betalist Tools
                elif name == "get_betalist_featured":
                    response = await self.betalist_fetcher.fetch_featured(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_betalist_latest":
                    response = await self.betalist_fetcher.fetch_latest(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_betalist_by_topic":
                    response = await self.betalist_fetcher.fetch_by_topic(
                        topic=arguments.get("topic", ""),
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Twitter/X Tools
                elif name == "get_twitter_hashtag_tweets":
                    response = await self.twitter_fetcher.fetch_hashtag_tweets(
                        hashtag=arguments.get("hashtag", ""),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_twitter_user_tweets":
                    response = await self.twitter_fetcher.fetch_user_tweets(
                        username=arguments.get("username", ""),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_twitter_tech_tweets":
                    response = await self.twitter_fetcher.fetch_tech_tweets(
                        limit=arguments.get("limit", 30),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_twitter_indie_hackers":
                    response = await self.twitter_fetcher.fetch_indie_hackers_tweets(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_twitter_user_profile":
                    response = await self.twitter_fetcher.fetch_user_profile(
                        username=arguments.get("username", ""),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                # Gumroad Tools
                elif name == "get_gumroad_discover":
                    response = await self.gumroad_fetcher.fetch_discover_products(
                        category=arguments.get("category"),
                        sort=arguments.get("sort", "featured"),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_gumroad_programming":
                    response = await self.gumroad_fetcher.fetch_programming_products(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_gumroad_design":
                    response = await self.gumroad_fetcher.fetch_design_products(
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "search_gumroad":
                    response = await self.gumroad_fetcher.search_products(
                        query=arguments.get("query", ""),
                        limit=arguments.get("limit", 20),
                        use_cache=arguments.get("use_cache", True),
                    )
                    return [TextContent(type="text", text=self._format_response(response))]

                elif name == "get_gumroad_creator":
                    response = await self.gumroad_fetcher.fetch_creator_products(
                        creator_username=arguments.get("username", ""),
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
        # await self.reddit_fetcher.close()  # Disabled: Requires Reddit API credentials
        await self.openrouter_fetcher.close()
        await self.trustmrr_fetcher.close()
        await self.aitools_fetcher.close()
        await self.huggingface_fetcher.close()
        await self.v2ex_fetcher.close()
        await self.juejin_fetcher.close()
        await self.devto_fetcher.close()
        await self.modelscope_fetcher.close()
        await self.stackoverflow_fetcher.close()
        await self.awesome_fetcher.close()
        await self.vscode_fetcher.close()
        await self.npm_fetcher.close()
        await self.chrome_fetcher.close()
        await self.pypi_fetcher.close()
        await self.remoteok_fetcher.close()
        await self.wordpress_fetcher.close()
        await self.lobsters_fetcher.close()
        await self.echojs_fetcher.close()
        await self.weworkremotely_fetcher.close()
        await self.paperswithcode_fetcher.close()
        await self.alternativeto_fetcher.close()
        await self.replicate_fetcher.close()
        await self.betalist_fetcher.close()


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

"""Cross-platform search and trending summary fetcher implementation."""

import time
from datetime import datetime, timezone
from typing import Any

from ...models.base import TrendingResponse
from ...models.cross_platform import (
    CrossPlatformSearchResult,
    PlatformSummaryItem,
    SearchResultItem,
    TrendingSummary,
)
from ...utils import logger
from ..base import BaseFetcher


class CrossPlatformFetcher(BaseFetcher):
    """Fetcher for cross-platform search and trending summary."""

    # Platform configurations for search
    SEARCHABLE_PLATFORMS = {
        "github": {
            "display_name": "GitHub Trending",
            "category": "code",
            "weight": 1.5,
        },
        "hackernews": {
            "display_name": "Hacker News",
            "category": "news",
            "weight": 2.0,
        },
        "producthunt": {
            "display_name": "Product Hunt",
            "category": "products",
            "weight": 1.5,
        },
        "devto": {
            "display_name": "dev.to",
            "category": "articles",
            "weight": 1.0,
        },
        "lobsters": {
            "display_name": "Lobsters",
            "category": "news",
            "weight": 1.2,
        },
        "echojs": {
            "display_name": "Echo JS",
            "category": "news",
            "weight": 0.8,
        },
        "juejin": {
            "display_name": "掘金 (Juejin)",
            "category": "articles",
            "weight": 0.8,
        },
        "v2ex": {
            "display_name": "V2EX",
            "category": "community",
            "weight": 0.8,
        },
        "huggingface": {
            "display_name": "HuggingFace",
            "category": "ai",
            "weight": 1.2,
        },
        "paperswithcode": {
            "display_name": "Papers with Code",
            "category": "research",
            "weight": 1.0,
        },
        "arxiv": {
            "display_name": "arXiv",
            "category": "research",
            "weight": 1.0,
        },
        "betalist": {
            "display_name": "Betalist",
            "category": "startups",
            "weight": 0.8,
        },
        "replicate": {
            "display_name": "Replicate",
            "category": "ai",
            "weight": 1.0,
        },
        "npm": {
            "display_name": "npm",
            "category": "packages",
            "weight": 0.8,
        },
        "pypi": {
            "display_name": "PyPI",
            "category": "packages",
            "weight": 0.8,
        },
        "vscode": {
            "display_name": "VS Code Extensions",
            "category": "tools",
            "weight": 0.8,
        },
        "wordpress": {
            "display_name": "WordPress Plugins",
            "category": "tools",
            "weight": 0.6,
        },
        "gumroad": {
            "display_name": "Gumroad",
            "category": "products",
            "weight": 0.8,
        },
        "indiehackers": {
            "display_name": "Indie Hackers",
            "category": "community",
            "weight": 1.0,
        },
    }

    # Platforms for trending summary
    SUMMARY_PLATFORMS = [
        "github",
        "hackernews",
        "producthunt",
        "devto",
        "lobsters",
        "huggingface",
        "paperswithcode",
        "betalist",
        "indiehackers",
        "v2ex",
        "juejin",
    ]

    def __init__(self, cache=None, **fetchers):
        """Initialize with references to other fetchers."""
        super().__init__(cache=cache)
        self.fetchers = fetchers

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "cross_platform"

    async def search_all_platforms(
        self,
        query: str,
        platforms: list[str] | None = None,
        limit_per_platform: int = 10,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Search across multiple platforms for a given query.

        Args:
            query: Search query string
            platforms: List of platforms to search (None = all available)
            limit_per_platform: Max results per platform
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with cross-platform search results
        """
        start_time = time.time()
        cache_key = f"cross_platform:search:{query}:{platforms}:{limit_per_platform}"

        if use_cache:
            cached = self._get_cached_response(cache_key)
            if cached:
                return cached

        try:
            logger.info(f"Cross-platform search: '{query}'")

            # Determine which platforms to search
            search_platforms = platforms or list(self.SEARCHABLE_PLATFORMS.keys())
            available_platforms = [p for p in search_platforms if p in self.fetchers]

            result = CrossPlatformSearchResult(
                query=query,
                platforms_searched=available_platforms,
            )

            all_results: list[SearchResultItem] = []

            # Search each platform concurrently
            search_tasks = []
            for platform in available_platforms:
                task = self._search_platform(
                    platform, query, limit_per_platform, use_cache
                )
                search_tasks.append((platform, task))

            # Gather results
            for platform, task in search_tasks:
                try:
                    platform_results = await task
                    result.results_by_platform[platform] = len(platform_results)
                    all_results.extend(platform_results)
                except Exception as e:
                    logger.warning(f"Error searching {platform}: {e}")
                    result.results_by_platform[platform] = 0

            # Sort by score and take top results
            all_results.sort(key=lambda x: x.score, reverse=True)
            result.total_results = len(all_results)
            result.top_results = [r.to_dict() for r in all_results[:50]]

            # Calculate search time
            result.search_time_ms = (time.time() - start_time) * 1000

            # Generate summary
            result.summary = (
                f"Found {result.total_results} results for '{query}' "
                f"across {len(available_platforms)} platforms in {result.search_time_ms:.0f}ms. "
                f"Top platforms: {', '.join(sorted(result.results_by_platform.keys(), key=lambda k: result.results_by_platform[k], reverse=True)[:3])}"
            )

            response = self._create_response(
                success=True,
                data_type="cross_platform_search",
                data=[result],
                metadata={
                    "query": query,
                    "platforms_searched": available_platforms,
                    "total_results": result.total_results,
                },
            )

            if use_cache:
                self._cache_response(cache_key, response)
            return response

        except Exception as e:
            logger.error(f"Error in cross-platform search: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="cross_platform_search",
                data=[],
                error=str(e),
            )

    async def _search_platform(
        self,
        platform: str,
        query: str,
        limit: int,
        use_cache: bool,
    ) -> list[SearchResultItem]:
        """Search a single platform and return normalized results."""
        results: list[SearchResultItem] = []
        fetcher = self.fetchers.get(platform)
        if not fetcher:
            return results

        platform_config = self.SEARCHABLE_PLATFORMS.get(platform, {})
        weight = platform_config.get("weight", 1.0)

        try:
            # Platform-specific search logic
            if platform == "github":
                response = await fetcher.fetch_trending_repositories(
                    language=None, use_cache=use_cache
                )
                if response.success:
                    for repo in response.data:
                        if self._matches_query(query, repo.name, repo.description):
                            results.append(
                                SearchResultItem(
                                    platform="GitHub",
                                    title=repo.name,
                                    url=repo.url,
                                    description=repo.description,
                                    score=repo.stars * weight * 0.001,
                                    metadata={
                                        "stars": repo.stars,
                                        "language": repo.language,
                                        "forks": repo.forks,
                                    },
                                )
                            )

            elif platform == "hackernews":
                response = await fetcher.fetch_stories(
                    story_type="top", limit=100, use_cache=use_cache
                )
                if response.success:
                    for story in response.data:
                        if self._matches_query(query, story.title, getattr(story, "text", "")):
                            results.append(
                                SearchResultItem(
                                    platform="Hacker News",
                                    title=story.title,
                                    url=story.url or f"https://news.ycombinator.com/item?id={story.id}",
                                    description=None,
                                    score=story.score * weight * 0.1,
                                    metadata={
                                        "score": story.score,
                                        "comments": story.descendants,
                                    },
                                )
                            )

            elif platform == "devto":
                # Try searching with query as tag first
                response = await fetcher.fetch_articles(
                    tag=query.replace(" ", "").replace("-", ""),
                    per_page=limit,
                    use_cache=use_cache,
                )
                if response.success:
                    for article in response.data:
                        results.append(
                            SearchResultItem(
                                platform="dev.to",
                                title=article.title,
                                url=article.url,
                                description=article.description,
                                score=(article.positive_reactions_count or 0) * weight * 0.1,
                                metadata={
                                    "reactions": article.positive_reactions_count,
                                    "comments": article.comments_count,
                                    "author": article.user_name,
                                },
                            )
                        )

            elif platform == "lobsters":
                response = await fetcher.fetch_hottest(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for story in response.data:
                        if self._matches_query(query, story.title, story.description or ""):
                            results.append(
                                SearchResultItem(
                                    platform="Lobsters",
                                    title=story.title,
                                    url=story.url,
                                    description=story.description,
                                    score=story.score * weight * 0.1,
                                    metadata={
                                        "score": story.score,
                                        "comments": story.comment_count,
                                        "tags": story.tags,
                                    },
                                )
                            )

            elif platform == "echojs":
                response = await fetcher.fetch_top(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for news in response.data:
                        if self._matches_query(query, news.title, ""):
                            results.append(
                                SearchResultItem(
                                    platform="Echo JS",
                                    title=news.title,
                                    url=news.url,
                                    description=None,
                                    score=(news.up - news.down) * weight * 0.1,
                                    metadata={
                                        "upvotes": news.up,
                                        "downvotes": news.down,
                                        "comments": news.comments,
                                    },
                                )
                            )

            elif platform == "juejin":
                response = await fetcher.fetch_recommended_articles(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for article in response.data:
                        if self._matches_query(query, article.title, article.brief_content or ""):
                            results.append(
                                SearchResultItem(
                                    platform="掘金",
                                    title=article.title,
                                    url=article.url,
                                    description=article.brief_content,
                                    score=article.digg_count * weight * 0.1,
                                    metadata={
                                        "diggs": article.digg_count,
                                        "views": article.view_count,
                                        "comments": article.comment_count,
                                    },
                                )
                            )

            elif platform == "v2ex":
                response = await fetcher.fetch_hot_topics(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for topic in response.data:
                        if self._matches_query(query, topic.title, topic.content or ""):
                            results.append(
                                SearchResultItem(
                                    platform="V2EX",
                                    title=topic.title,
                                    url=topic.url,
                                    description=topic.content[:200] if topic.content else None,
                                    score=topic.replies * weight * 0.5,
                                    metadata={
                                        "replies": topic.replies,
                                        "node": topic.node_name,
                                    },
                                )
                            )

            elif platform == "huggingface":
                response = await fetcher.fetch_trending_models(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for model in response.data:
                        # HFModel uses 'id' not 'model_id'
                        if self._matches_query(query, model.id, model.pipeline_tag or ""):
                            results.append(
                                SearchResultItem(
                                    platform="HuggingFace",
                                    title=model.id,
                                    url=f"https://huggingface.co/{model.id}",
                                    description=model.pipeline_tag,
                                    score=model.downloads * weight * 0.00001,
                                    metadata={
                                        "downloads": model.downloads,
                                        "likes": model.likes,
                                        "task": model.pipeline_tag,
                                    },
                                )
                            )

            elif platform == "paperswithcode":
                # Use search if query provided
                response = await fetcher.search_papers(
                    query=query, limit=limit, use_cache=use_cache
                )
                if response.success:
                    for paper in response.data:
                        results.append(
                            SearchResultItem(
                                platform="Papers with Code",
                                title=paper.title,
                                url=paper.url_abs or paper.paper_url or "",
                                description=paper.abstract[:300] if paper.abstract else None,
                                score=(paper.stars or 0) * weight * 0.01,
                                metadata={
                                    "stars": paper.stars,
                                    "authors": paper.authors[:3] if paper.authors else [],
                                },
                            )
                        )

            elif platform == "arxiv":
                response = await fetcher.fetch_papers(
                    search_query=query, limit=limit, use_cache=use_cache
                )
                if response.success:
                    for paper in response.data:
                        results.append(
                            SearchResultItem(
                                platform="arXiv",
                                title=paper.title,
                                url=paper.url,
                                description=paper.summary[:300] if paper.summary else None,
                                score=weight * 10,  # arXiv doesn't have popularity metrics
                                metadata={
                                    "authors": paper.authors[:3] if paper.authors else [],
                                    "category": paper.primary_category,
                                },
                            )
                        )

            elif platform == "betalist":
                response = await fetcher.fetch_featured(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for startup in response.data:
                        if self._matches_query(query, startup.name, startup.tagline or ""):
                            results.append(
                                SearchResultItem(
                                    platform="Betalist",
                                    title=startup.name,
                                    url=startup.url,
                                    description=startup.tagline,
                                    score=weight * 10,
                                    metadata={
                                        "topics": startup.topics[:3] if startup.topics else [],
                                    },
                                )
                            )

            elif platform == "replicate":
                response = await fetcher.fetch_trending_models(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for model in response.data:
                        if self._matches_query(query, model.name, model.description or ""):
                            results.append(
                                SearchResultItem(
                                    platform="Replicate",
                                    title=model.name,
                                    url=model.url,
                                    description=model.description,
                                    score=model.run_count * weight * 0.0001,
                                    metadata={
                                        "runs": model.run_count,
                                        "owner": model.owner,
                                    },
                                )
                            )

            elif platform == "npm":
                response = await fetcher.fetch_trending_packages(
                    category=query, limit=limit, use_cache=use_cache
                )
                if response.success:
                    for pkg in response.data:
                        results.append(
                            SearchResultItem(
                                platform="npm",
                                title=pkg.name,
                                url=f"https://www.npmjs.com/package/{pkg.name}",
                                description=pkg.description,
                                score=(pkg.downloads_week or 0) * weight * 0.00001,
                                metadata={
                                    "downloads_week": pkg.downloads_week,
                                    "version": pkg.version,
                                },
                            )
                        )

            elif platform == "pypi":
                response = await fetcher.fetch_trending_packages(
                    category=query, limit=limit, use_cache=use_cache
                )
                if response.success:
                    for pkg in response.data:
                        results.append(
                            SearchResultItem(
                                platform="PyPI",
                                title=pkg.name,
                                url=f"https://pypi.org/project/{pkg.name}/",
                                description=pkg.summary,
                                score=(pkg.downloads or 0) * weight * 0.00001,
                                metadata={
                                    "downloads": pkg.downloads,
                                    "version": pkg.version,
                                },
                            )
                        )

            elif platform == "vscode":
                response = await fetcher.fetch_trending_extensions(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for ext in response.data:
                        if self._matches_query(query, ext.extension_name, ext.short_description):
                            results.append(
                                SearchResultItem(
                                    platform="VS Code",
                                    title=ext.extension_name,
                                    url=f"https://marketplace.visualstudio.com/items?itemName={ext.extension_id}",
                                    description=ext.short_description,
                                    score=ext.install_count * weight * 0.00001,
                                    metadata={
                                        "installs": ext.install_count,
                                        "rating": ext.average_rating,
                                        "publisher": ext.publisher_display_name,
                                    },
                                )
                            )

            elif platform == "gumroad":
                response = await fetcher.search_products(
                    query=query, limit=limit, use_cache=use_cache
                )
                if response.success:
                    for product in response.data:
                        results.append(
                            SearchResultItem(
                                platform="Gumroad",
                                title=product.name,
                                url=product.url,
                                description=product.description,
                                score=weight * 10,
                                metadata={
                                    "price": product.price,
                                    "creator": product.creator.name if product.creator else None,
                                },
                            )
                        )

            elif platform == "producthunt":
                response = await fetcher.fetch_products(
                    time_range="today", limit=50, use_cache=use_cache
                )
                if response.success:
                    for product in response.data:
                        if self._matches_query(query, product.name, product.tagline or ""):
                            results.append(
                                SearchResultItem(
                                    platform="Product Hunt",
                                    title=product.name,
                                    url=product.url,
                                    description=product.tagline,
                                    score=product.votes_count * weight * 0.1,
                                    metadata={
                                        "votes": product.votes_count,
                                        "comments": product.comments_count,
                                    },
                                )
                            )

            elif platform == "indiehackers":
                response = await fetcher.fetch_popular_posts(
                    limit=50, use_cache=use_cache
                )
                if response.success:
                    for post in response.data:
                        if self._matches_query(query, post.title, getattr(post, "content", "") or ""):
                            results.append(
                                SearchResultItem(
                                    platform="Indie Hackers",
                                    title=post.title,
                                    url=post.url,
                                    description=None,
                                    score=post.reply_count * weight * 0.5,
                                    metadata={
                                        "replies": post.reply_count,
                                        "views": post.view_count,
                                    },
                                )
                            )

        except Exception as e:
            logger.warning(f"Error searching {platform}: {e}")

        return results[:limit]

    def _matches_query(self, query: str, *texts: str | None) -> bool:
        """Check if any of the texts contain the query (case-insensitive)."""
        query_lower = query.lower()
        query_parts = query_lower.split()

        for text in texts:
            if text:
                text_lower = text.lower()
                # Match if all query parts are found
                if all(part in text_lower for part in query_parts):
                    return True
        return False

    async def get_trending_summary(
        self,
        platforms: list[str] | None = None,
        items_per_platform: int = 5,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Get today's trending summary across all platforms.

        Args:
            platforms: List of platforms to include (None = all)
            items_per_platform: Number of top items per platform
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with trending summary
        """
        cache_key = f"cross_platform:summary:{platforms}:{items_per_platform}"

        if use_cache:
            cached = self._get_cached_response(cache_key)
            if cached:
                return cached

        try:
            logger.info("Generating trending summary")

            summary_platforms = platforms or self.SUMMARY_PLATFORMS
            available_platforms = [p for p in summary_platforms if p in self.fetchers]

            summary = TrendingSummary(
                generated_at=datetime.now(timezone.utc).isoformat(),
                total_platforms=len(available_platforms),
            )

            categories: dict[str, int] = {}
            all_highlights: list[str] = []

            # Fetch from each platform concurrently
            fetch_tasks = []
            for platform in available_platforms:
                task = self._fetch_platform_summary(
                    platform, items_per_platform, use_cache
                )
                fetch_tasks.append((platform, task))

            for platform, task in fetch_tasks:
                try:
                    platform_summary = await task
                    summary.platform_summaries.append(platform_summary)
                    summary.total_items += platform_summary.item_count

                    # Track categories
                    platform_config = self.SEARCHABLE_PLATFORMS.get(platform, {})
                    category = platform_config.get("category", "other")
                    categories[category] = categories.get(category, 0) + platform_summary.item_count

                    # Collect highlights
                    all_highlights.extend(platform_summary.highlights[:2])

                except Exception as e:
                    logger.warning(f"Error fetching {platform} summary: {e}")
                    summary.platform_summaries.append(
                        PlatformSummaryItem(
                            platform=platform,
                            platform_display_name=self.SEARCHABLE_PLATFORMS.get(platform, {}).get(
                                "display_name", platform
                            ),
                            fetch_success=False,
                            error_message=str(e),
                        )
                    )

            summary.categories = categories
            summary.top_highlights = all_highlights[:10]

            # Generate summary text
            successful_platforms = [
                p for p in summary.platform_summaries if p.fetch_success
            ]
            summary.summary_text = (
                f"📊 Today's Trending Summary ({summary.generated_at[:10]})\n\n"
                f"Analyzed {len(successful_platforms)} platforms with {summary.total_items} trending items.\n\n"
                f"📈 Categories: {', '.join(f'{k}: {v}' for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5])}\n\n"
                f"🔥 Top Highlights:\n" + "\n".join(f"  • {h}" for h in summary.top_highlights[:5])
            )

            response = self._create_response(
                success=True,
                data_type="trending_summary",
                data=[summary],
                metadata={
                    "platforms_included": len(successful_platforms),
                    "total_items": summary.total_items,
                    "generated_at": summary.generated_at,
                },
            )

            if use_cache:
                self._cache_response(cache_key, response)
            return response

        except Exception as e:
            logger.error(f"Error generating trending summary: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_summary",
                data=[],
                error=str(e),
            )

    async def _fetch_platform_summary(
        self,
        platform: str,
        limit: int,
        use_cache: bool,
    ) -> PlatformSummaryItem:
        """Fetch summary from a single platform."""
        platform_config = self.SEARCHABLE_PLATFORMS.get(platform, {})
        display_name = platform_config.get("display_name", platform)

        summary = PlatformSummaryItem(
            platform=platform,
            platform_display_name=display_name,
        )

        fetcher = self.fetchers.get(platform)
        if not fetcher:
            summary.fetch_success = False
            summary.error_message = "Fetcher not available"
            return summary

        try:
            # Platform-specific fetch logic
            if platform == "github":
                response = await fetcher.fetch_trending_repositories(
                    use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for repo in response.data[:limit]:
                        summary.top_items.append({
                            "title": repo.name,
                            "url": repo.url,
                            "stars": repo.stars,
                            "language": repo.language,
                        })
                        summary.highlights.append(
                            f"[GitHub] {repo.name} ⭐{repo.stars:,} - {repo.description[:50] if repo.description else 'No description'}..."
                        )

            elif platform == "hackernews":
                response = await fetcher.fetch_stories(
                    story_type="top", limit=30, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for story in response.data[:limit]:
                        summary.top_items.append({
                            "title": story.title,
                            "url": story.url,
                            "score": story.score,
                            "comments": story.descendants,
                        })
                        summary.highlights.append(
                            f"[HN] {story.title[:60]}... ({story.score} points)"
                        )

            elif platform == "producthunt":
                response = await fetcher.fetch_products(
                    time_range="today", limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for product in response.data[:limit]:
                        summary.top_items.append({
                            "title": product.name,
                            "url": product.url,
                            "tagline": product.tagline,
                            "votes": product.votes_count,
                        })
                        summary.highlights.append(
                            f"[PH] {product.name} - {product.tagline[:40] if product.tagline else ''}... ({product.votes_count} votes)"
                        )

            elif platform == "devto":
                response = await fetcher.fetch_articles(
                    per_page=30, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for article in response.data[:limit]:
                        summary.top_items.append({
                            "title": article.title,
                            "url": article.url,
                            "reactions": article.positive_reactions_count,
                        })
                        summary.highlights.append(
                            f"[dev.to] {article.title[:50]}... ({article.positive_reactions_count or 0} reactions)"
                        )

            elif platform == "lobsters":
                response = await fetcher.fetch_hottest(
                    limit=30, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for story in response.data[:limit]:
                        summary.top_items.append({
                            "title": story.title,
                            "url": story.url,
                            "score": story.score,
                        })
                        summary.highlights.append(
                            f"[Lobsters] {story.title[:50]}... ({story.score} points)"
                        )

            elif platform == "huggingface":
                response = await fetcher.fetch_trending_models(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for model in response.data[:limit]:
                        summary.top_items.append({
                            "title": model.id,
                            "downloads": model.downloads,
                            "task": model.pipeline_tag,
                        })
                        summary.highlights.append(
                            f"[HF] {model.id} ({model.downloads:,} downloads)"
                        )

            elif platform == "paperswithcode":
                response = await fetcher.fetch_trending_papers(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for paper in response.data[:limit]:
                        summary.top_items.append({
                            "title": paper.title,
                            "url": paper.url_abs or paper.paper_url,
                            "stars": paper.stars,
                        })
                        summary.highlights.append(
                            f"[Paper] {paper.title[:50]}... ({paper.stars or 0} ⭐)"
                        )

            elif platform == "betalist":
                response = await fetcher.fetch_featured(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for startup in response.data[:limit]:
                        summary.top_items.append({
                            "title": startup.name,
                            "url": startup.url,
                            "tagline": startup.tagline,
                        })
                        summary.highlights.append(
                            f"[Betalist] {startup.name} - {startup.tagline[:40] if startup.tagline else 'No tagline'}..."
                        )

            elif platform == "indiehackers":
                response = await fetcher.fetch_popular_posts(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for post in response.data[:limit]:
                        summary.top_items.append({
                            "title": post.title,
                            "url": post.url,
                            "replies": post.reply_count,
                        })
                        summary.highlights.append(
                            f"[IH] {post.title[:50]}... ({post.reply_count} replies)"
                        )

            elif platform == "v2ex":
                response = await fetcher.fetch_hot_topics(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for topic in response.data[:limit]:
                        summary.top_items.append({
                            "title": topic.title,
                            "url": topic.url,
                            "replies": topic.replies,
                        })
                        summary.highlights.append(
                            f"[V2EX] {topic.title[:50]}... ({topic.replies} replies)"
                        )

            elif platform == "juejin":
                response = await fetcher.fetch_recommended_articles(
                    limit=20, use_cache=use_cache
                )
                if response.success:
                    summary.item_count = len(response.data)
                    for article in response.data[:limit]:
                        summary.top_items.append({
                            "title": article.title,
                            "url": article.url,
                            "diggs": article.digg_count,
                        })
                        summary.highlights.append(
                            f"[掘金] {article.title[:50]}... ({article.digg_count} 赞)"
                        )

            summary.fetch_success = True

        except Exception as e:
            logger.warning(f"Error fetching {platform} summary: {e}")
            summary.fetch_success = False
            summary.error_message = str(e)

        return summary

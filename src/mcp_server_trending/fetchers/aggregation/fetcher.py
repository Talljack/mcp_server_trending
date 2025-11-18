"""Aggregation analysis fetcher implementation."""

from typing import TYPE_CHECKING

from ...models.aggregation import IndieRevenueDashboard, TechStackAnalysis, TopicTrends
from ...models.base import TrendingResponse
from ...utils import logger
from ..base import BaseFetcher

if TYPE_CHECKING:
    from ..github import GitHubTrendingFetcher
    from ..npm import NPMFetcher
    from ..pypi import PyPIFetcher
    from ..remoteok import RemoteOKFetcher
    from ..stackoverflow import StackOverflowFetcher
    from ..vscode import VSCodeMarketplaceFetcher
    from ..indiehackers import IndieHackersFetcher
    from ..trustmrr import TrustMRRFetcher
    from ..hackernews import HackerNewsFetcher
    from ..devto import DevToFetcher
    from ..juejin import JuejinFetcher


class AggregationFetcher(BaseFetcher):
    """Fetcher for cross-platform aggregation analysis."""

    def __init__(self, cache=None, **fetchers):
        """Initialize with references to other fetchers."""
        super().__init__(cache=cache)
        self.fetchers = fetchers

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "aggregation"

    async def analyze_tech_stack(
        self,
        tech: str,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Analyze technology stack popularity across platforms.

        Args:
            tech: Technology name (e.g., 'nextjs', 'python', 'react')
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with tech stack analysis
        """
        try:
            logger.info(f"Analyzing tech stack: {tech}")

            analysis = TechStackAnalysis(tech_name=tech)

            # GitHub repos
            if "github" in self.fetchers:
                try:
                    response = await self.fetchers["github"].fetch_trending_repositories(
                        language=tech, use_cache=use_cache
                    )
                    if response.success:
                        analysis.github_repos = len(response.data)
                except Exception as e:
                    logger.warning(f"Error fetching GitHub data: {e}")

            # npm packages
            if "npm" in self.fetchers:
                try:
                    response = await self.fetchers["npm"].fetch_trending_packages(
                        category=tech, limit=10, use_cache=use_cache
                    )
                    if response.success:
                        analysis.npm_packages = len(response.data)
                except Exception as e:
                    logger.warning(f"Error fetching npm data: {e}")

            # PyPI packages
            if "pypi" in self.fetchers:
                try:
                    response = await self.fetchers["pypi"].fetch_trending_packages(
                        category=tech, limit=10, use_cache=use_cache
                    )
                    if response.success:
                        analysis.pypi_packages = len(response.data)
                except Exception as e:
                    logger.warning(f"Error fetching PyPI data: {e}")

            # Stack Overflow
            if "stackoverflow" in self.fetchers:
                try:
                    # Search for tags containing the tech name
                    response = await self.fetchers["stackoverflow"].fetch_tags(
                        limit=100, use_cache=use_cache
                    )
                    if response.success:
                        # Count tags matching the tech name
                        matching_tags = [
                            tag
                            for tag in response.data
                            if tech.lower() in tag.name.lower()
                        ]
                        if matching_tags:
                            analysis.stackoverflow_questions = sum(
                                tag.count for tag in matching_tags[:5]
                            )
                except Exception as e:
                    logger.warning(f"Error fetching Stack Overflow data: {e}")

            # VS Code extensions
            if "vscode" in self.fetchers:
                try:
                    response = await self.fetchers["vscode"].fetch_trending_extensions(
                        limit=50, use_cache=use_cache
                    )
                    if response.success:
                        # Count extensions related to the tech
                        matching_extensions = [
                            ext
                            for ext in response.data
                            if tech.lower() in ext.extension_name.lower()
                            or tech.lower() in ext.short_description.lower()
                        ]
                        analysis.vscode_extensions = len(matching_extensions)
                except Exception as e:
                    logger.warning(f"Error fetching VS Code data: {e}")

            # Job postings
            if "remoteok" in self.fetchers:
                try:
                    response = await self.fetchers["remoteok"].fetch_jobs(
                        tags=[tech], limit=100, use_cache=use_cache
                    )
                    if response.success:
                        analysis.job_postings = len(response.data)
                except Exception as e:
                    logger.warning(f"Error fetching RemoteOK data: {e}")

            # Calculate total score
            analysis.total_score = (
                analysis.github_repos * 1.0
                + analysis.npm_packages * 0.8
                + analysis.pypi_packages * 0.8
                + analysis.stackoverflow_questions * 0.001
                + analysis.vscode_extensions * 0.5
                + analysis.job_postings * 2.0
            )

            # Generate summary
            analysis.summary = (
                f"{tech} analysis: "
                f"{analysis.github_repos} GitHub repos, "
                f"{analysis.npm_packages + analysis.pypi_packages} packages, "
                f"{analysis.stackoverflow_questions:,} SO questions, "
                f"{analysis.vscode_extensions} VS Code extensions, "
                f"{analysis.job_postings} job postings"
            )

            return self._create_response(
                success=True,
                data_type="tech_stack_analysis",
                data=[analysis],
                metadata={"tech": tech, "platforms_analyzed": list(self.fetchers.keys())},
            )

        except Exception as e:
            logger.error(f"Error in tech stack analysis: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="tech_stack_analysis",
                data=[],
                error=str(e),
            )

    async def get_indie_revenue_dashboard(
        self,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Get indie developer revenue dashboard.

        Args:
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with revenue dashboard
        """
        try:
            logger.info("Generating indie revenue dashboard")

            dashboard = IndieRevenueDashboard()
            all_projects = []

            # Indie Hackers income reports
            if "indiehackers" in self.fetchers:
                try:
                    response = await self.fetchers["indiehackers"].fetch_income_reports(
                        limit=50, use_cache=use_cache
                    )
                    if response.success:
                        all_projects.extend(response.data)
                        dashboard.data_sources.append("Indie Hackers")
                except Exception as e:
                    logger.warning(f"Error fetching Indie Hackers data: {e}")

            # TrustMRR rankings
            if "trustmrr" in self.fetchers:
                try:
                    response = await self.fetchers["trustmrr"].fetch_rankings(
                        limit=50, use_cache=use_cache
                    )
                    if response.success:
                        dashboard.data_sources.append("TrustMRR")
                        # Note: TrustMRR data structure might be different
                except Exception as e:
                    logger.warning(f"Error fetching TrustMRR data: {e}")

            # Calculate metrics
            dashboard.total_projects = len(all_projects)

            if all_projects:
                # Calculate average MRR (from Indie Hackers data)
                mrr_values = []
                for proj in all_projects:
                    if hasattr(proj, "revenue") and proj.revenue:
                        # Ensure revenue is numeric
                        try:
                            revenue_value = float(proj.revenue) if isinstance(proj.revenue, (str, int, float)) else 0
                            if revenue_value > 0:
                                mrr_values.append(revenue_value)
                        except (ValueError, TypeError):
                            continue

                if mrr_values:
                    dashboard.average_mrr = sum(mrr_values) / len(mrr_values)

                # Find success stories (>$10k MRR)
                success_count = 0
                for proj in all_projects:
                    if hasattr(proj, "revenue") and proj.revenue:
                        try:
                            revenue_value = float(proj.revenue) if isinstance(proj.revenue, (str, int, float)) else 0
                            if revenue_value > 10000:
                                success_count += 1
                        except (ValueError, TypeError):
                            continue
                dashboard.success_stories_count = success_count

                # Get top categories
                categories = {}
                for proj in all_projects:
                    if hasattr(proj, "category") and proj.category:
                        categories[proj.category] = categories.get(proj.category, 0) + 1

                dashboard.top_categories = sorted(categories, key=categories.get, reverse=True)[:5]

            # Generate summary
            dashboard.summary = (
                f"Indie Revenue Dashboard: {dashboard.total_projects} projects tracked, "
                f"${dashboard.average_mrr:,.0f} average MRR, "
                f"{dashboard.success_stories_count} success stories (>$10k MRR)"
            )

            return self._create_response(
                success=True,
                data_type="indie_revenue_dashboard",
                data=[dashboard],
                metadata={"data_sources": dashboard.data_sources},
            )

        except Exception as e:
            logger.error(f"Error generating indie revenue dashboard: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="indie_revenue_dashboard",
                data=[],
                error=str(e),
            )

    async def track_topic_trends(
        self,
        topic: str,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Track topic trends across multiple platforms.

        Args:
            topic: Topic to track (e.g., 'ai-agents', 'web3', 'serverless')
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with topic trends
        """
        try:
            logger.info(f"Tracking topic trends: {topic}")

            trends = TopicTrends(topic=topic)

            # Hacker News
            if "hackernews" in self.fetchers:
                try:
                    response = await self.fetchers["hackernews"].fetch_stories(
                        story_type="top", limit=100, use_cache=use_cache
                    )
                    if response.success:
                        # Count stories mentioning the topic
                        matching_stories = [
                            story
                            for story in response.data
                            if topic.lower() in story.title.lower()
                        ]
                        trends.hackernews_mentions = len(matching_stories)
                except Exception as e:
                    logger.warning(f"Error fetching Hacker News data: {e}")

            # GitHub
            if "github" in self.fetchers:
                try:
                    response = await self.fetchers["github"].fetch_trending_repositories(
                        use_cache=use_cache
                    )
                    if response.success:
                        # Count repos related to topic
                        matching_repos = [
                            repo
                            for repo in response.data
                            if topic.lower() in repo.name.lower()
                            or topic.lower() in repo.description.lower()
                        ]
                        trends.github_repos = len(matching_repos)
                except Exception as e:
                    logger.warning(f"Error fetching GitHub data: {e}")

            # Stack Overflow
            if "stackoverflow" in self.fetchers:
                try:
                    response = await self.fetchers["stackoverflow"].fetch_tags(
                        limit=100, use_cache=use_cache
                    )
                    if response.success:
                        # Find matching tags
                        matching_tags = [
                            tag
                            for tag in response.data
                            if topic.lower() in tag.name.lower()
                        ]
                        if matching_tags:
                            trends.stackoverflow_tags = sum(tag.count for tag in matching_tags[:3])
                except Exception as e:
                    logger.warning(f"Error fetching Stack Overflow data: {e}")

            # dev.to articles
            if "devto" in self.fetchers:
                try:
                    # Try to fetch with topic as tag
                    response = await self.fetchers["devto"].fetch_articles(
                        tag=topic.replace("-", ""), per_page=30, use_cache=use_cache
                    )
                    if response.success:
                        trends.dev_articles = len(response.data)
                except Exception as e:
                    logger.warning(f"Error fetching dev.to data: {e}")

            # Juejin articles
            if "juejin" in self.fetchers:
                try:
                    response = await self.fetchers["juejin"].fetch_recommended_articles(
                        limit=30, use_cache=use_cache
                    )
                    if response.success:
                        # Count articles mentioning topic
                        matching_articles = [
                            article
                            for article in response.data
                            if topic.lower() in article.title.lower()
                        ]
                        trends.juejin_articles = len(matching_articles)
                except Exception as e:
                    logger.warning(f"Error fetching Juejin data: {e}")

            # Calculate totals
            trends.total_mentions = (
                trends.hackernews_mentions
                + trends.github_repos
                + trends.dev_articles
                + trends.juejin_articles
            )

            trends.trending_score = (
                trends.hackernews_mentions * 2.0
                + trends.github_repos * 1.5
                + trends.stackoverflow_tags * 0.0001
                + trends.dev_articles * 1.0
                + trends.juejin_articles * 1.0
            )

            # Generate summary
            trends.summary = (
                f"{topic} trending: "
                f"{trends.hackernews_mentions} HN mentions, "
                f"{trends.github_repos} GitHub repos, "
                f"{trends.stackoverflow_tags:,} SO tags, "
                f"{trends.dev_articles} dev.to articles, "
                f"{trends.juejin_articles} Juejin articles"
            )

            return self._create_response(
                success=True,
                data_type="topic_trends",
                data=[trends],
                metadata={"topic": topic, "total_mentions": trends.total_mentions},
            )

        except Exception as e:
            logger.error(f"Error tracking topic trends: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="topic_trends",
                data=[],
                error=str(e),
            )

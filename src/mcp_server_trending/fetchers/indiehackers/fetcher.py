"""Indie Hackers fetcher implementation."""

import re
from datetime import datetime

from bs4 import BeautifulSoup

from ...models import IncomeReport, IndieHackersPost, ProjectMilestone, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class IndieHackersFetcher(BaseFetcher):
    """Fetcher for Indie Hackers trending content."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://www.indiehackers.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "indiehackers"

    async def fetch_popular_posts(
        self, limit: int = 30, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch popular posts from Indie Hackers.

        Args:
            limit: Number of posts to fetch (default: 30)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with popular posts
        """
        return await self.fetch_with_cache(
            data_type="popular_posts",
            fetch_func=self._fetch_popular_posts_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_popular_posts_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch popular posts."""
        try:
            url = f"{self.base_url}/posts/popular/all-time"
            response = await self.http_client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            posts = self._parse_posts(soup, limit)

            return self._create_response(
                success=True,
                data_type="popular_posts",
                data=posts,
                metadata={"total_count": len(posts), "limit": limit},
            )

        except Exception as e:
            logger.error(f"Error fetching Indie Hackers popular posts: {e}")
            return self._create_response(success=False, data_type="popular_posts", error=str(e))

    async def fetch_income_reports(
        self, limit: int = 30, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch income reports from Indie Hackers.

        Args:
            limit: Number of reports to fetch (default: 30)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with income reports
        """
        return await self.fetch_with_cache(
            data_type="income_reports",
            fetch_func=self._fetch_income_reports_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_income_reports_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch income reports."""
        try:
            # Indie Hackers doesn't have a dedicated income reports page
            # We'll scrape from the main posts and filter by revenue-related tags
            url = f"{self.base_url}/posts"
            response = await self.http_client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            reports = self._parse_income_reports(soup, limit)

            return self._create_response(
                success=True,
                data_type="income_reports",
                data=reports,
                metadata={"total_count": len(reports), "limit": limit},
            )

        except Exception as e:
            logger.error(f"Error fetching Indie Hackers income reports: {e}")
            return self._create_response(success=False, data_type="income_reports", error=str(e))

    async def fetch_milestones(self, limit: int = 30, use_cache: bool = True) -> TrendingResponse:
        """
        Fetch project milestones from Indie Hackers.

        Args:
            limit: Number of milestones to fetch (default: 30)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with project milestones
        """
        return await self.fetch_with_cache(
            data_type="milestones",
            fetch_func=self._fetch_milestones_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_milestones_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch milestones."""
        try:
            url = f"{self.base_url}/products"
            response = await self.http_client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            milestones = self._parse_milestones(soup, limit)

            return self._create_response(
                success=True,
                data_type="milestones",
                data=milestones,
                metadata={"total_count": len(milestones), "limit": limit},
            )

        except Exception as e:
            logger.error(f"Error fetching Indie Hackers milestones: {e}")
            return self._create_response(success=False, data_type="milestones", error=str(e))

    def _parse_posts(self, soup: BeautifulSoup, limit: int) -> list[IndieHackersPost]:
        """Parse posts from HTML."""
        posts = []
        rank = 1

        # Indie Hackers structure may vary, this is a simplified parser
        # You'll need to inspect the actual HTML to refine selectors
        post_elements = soup.select(".post-item, article")[:limit]

        for element in post_elements:
            try:
                # Extract post data (adjust selectors based on actual HTML)
                title_elem = element.select_one("h2, h3, .post-title")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = title_elem.find("a")
                url = link.get("href", "") if link else ""
                if url and not url.startswith("http"):
                    url = self.base_url + url

                # Extract author
                author_elem = element.select_one(".post-author, .author")
                author = author_elem.get_text(strip=True) if author_elem else "Unknown"
                author_url = ""
                if author_elem and author_elem.find("a"):
                    author_url = author_elem.find("a").get("href", "")
                    if author_url and not author_url.startswith("http"):
                        author_url = self.base_url + author_url

                # Extract preview
                preview_elem = element.select_one(".post-preview, .excerpt, p")
                content_preview = preview_elem.get_text(strip=True)[:200] if preview_elem else ""

                # Extract metrics
                upvotes_elem = element.select_one(".upvotes, .votes")
                upvotes = self._parse_number(upvotes_elem.get_text() if upvotes_elem else "0")

                comments_elem = element.select_one(".comments-count")
                comments_count = self._parse_number(
                    comments_elem.get_text() if comments_elem else "0"
                )

                # Create post object
                post = IndieHackersPost(
                    rank=rank,
                    id=url.split("/")[-1] if url else f"post-{rank}",
                    title=title,
                    url=url,
                    author=author,
                    author_url=author_url,
                    content_preview=content_preview,
                    upvotes=upvotes,
                    comments_count=comments_count,
                    created_at=datetime.now(),  # Would need to parse actual date
                    post_type="post",
                    tags=[],
                )

                posts.append(post)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing post: {e}")
                continue

        return posts

    def _parse_income_reports(self, soup: BeautifulSoup, limit: int) -> list[IncomeReport]:
        """Parse income reports from HTML."""
        reports = []
        rank = 1

        # This is a placeholder implementation
        # Actual implementation would require inspecting Indie Hackers HTML
        report_elements = soup.select(".income-report, .revenue-post")[:limit]

        for element in report_elements:
            try:
                # Extract revenue information
                title_elem = element.select_one("h2, h3")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                # Parse revenue from title or content
                revenue_match = re.search(r"\$[\d,]+(?:k|K)?(?:/mo|/month|/yr)?", title)
                revenue = revenue_match.group() if revenue_match else "Unknown"

                report = IncomeReport(
                    rank=rank,
                    project_name=title,
                    project_url="",
                    author="Unknown",
                    author_url="",
                    revenue=revenue,
                    description=title,
                )

                reports.append(report)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing income report: {e}")
                continue

        return reports

    def _parse_milestones(self, soup: BeautifulSoup, limit: int) -> list[ProjectMilestone]:
        """Parse milestones from HTML."""
        milestones = []
        rank = 1

        # Placeholder implementation
        milestone_elements = soup.select(".milestone, .product-milestone")[:limit]

        for element in milestone_elements:
            try:
                milestone = ProjectMilestone(
                    rank=rank,
                    project_name="Project",
                    project_url="",
                    author="Unknown",
                    author_url="",
                    milestone_type="Achievement",
                    milestone_value="",
                    description="",
                    achieved_at=datetime.now(),
                )

                milestones.append(milestone)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing milestone: {e}")
                continue

        return milestones

    def _parse_number(self, text: str) -> int:
        """Parse number from text (e.g., '1.2k' -> 1200)."""
        text = text.strip().lower().replace(",", "")
        if "k" in text:
            return int(float(text.replace("k", "")) * 1000)
        try:
            return int(float(text))
        except (ValueError, AttributeError):
            return 0

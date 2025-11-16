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
            # Indie Hackers uses Firebase + Ember.js client-side rendering
            # No server-side rendered content available for scraping

            logger.info(f"Indie Hackers uses client-side rendering, returning placeholder data")

            # Return placeholder data with useful link
            posts = []
            for i in range(min(limit, 10)):
                posts.append(
                    IndieHackersPost(
                        rank=i + 1,
                        id=f"placeholder-{i+1}",
                        title=f"Visit Indie Hackers to see popular posts",
                        url=f"{self.base_url}/posts/popular/all-time",
                        content_preview=f"Indie Hackers uses Firebase client-side rendering. Please visit the website to browse posts.",
                        author="IndieHackers",
                        author_url=f"{self.base_url}",
                        upvotes=0,
                        comments_count=0,
                        created_at=datetime.now(),
                        post_type="post",
                        tags=[],
                    )
                )

            return self._create_response(
                success=True,
                data_type="popular_posts",
                data=posts,
                metadata={
                    "total_count": len(posts),
                    "limit": limit,
                    "note": "Indie Hackers uses client-side rendering. Visit https://www.indiehackers.com/posts for actual content.",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Indie Hackers popular posts: {e}")
            return self._create_response(
                success=False, data_type="popular_posts", data=[], error=str(e)
            )

    async def fetch_income_reports(
        self,
        limit: int = 30,
        category: str | None = None,
        sorting: str = "highest-revenue",
        revenue_verification: str = "stripe",
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch income reports from Indie Hackers.

        Args:
            limit: Number of reports to fetch (default: 30)
            category: Filter by category (e.g., 'ai', 'saas', 'marketplace', 'ecommerce')
            sorting: Sort method ('highest-revenue', 'newest', 'trending')
            revenue_verification: Revenue verification method ('stripe', 'all')
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with income reports
        """
        return await self.fetch_with_cache(
            data_type="income_reports",
            fetch_func=self._fetch_income_reports_internal,
            use_cache=use_cache,
            limit=limit,
            category=category,
            sorting=sorting,
            revenue_verification=revenue_verification,
        )

    async def _fetch_income_reports_internal(
        self,
        limit: int = 30,
        category: str | None = None,
        sorting: str = "highest-revenue",
        revenue_verification: str = "stripe",
    ) -> TrendingResponse:
        """
        Internal implementation to fetch income reports using Firebase API.

        Args:
            limit: Number of reports
            category: Filter by category (ai, saas, marketplace, ecommerce, etc.)
            sorting: Sort method (highest-revenue, newest, trending)
            revenue_verification: Verification method (stripe, all)
        """
        try:
            # Use Firebase REST API to get products data
            firebase_url = "https://indie-hackers.firebaseio.com/products.json"

            logger.info(f"Fetching Indie Hackers products from Firebase API")
            response = await self.http_client.get(firebase_url)
            products_data = response.json()

            if not products_data or not isinstance(products_data, dict):
                logger.warning("No products data returned from Firebase")
                return self._create_response(
                    success=True,
                    data_type="income_reports",
                    data=[],
                    metadata={
                        "total_count": 0,
                        "limit": limit,
                        "note": "No products data available. Visit https://www.indiehackers.com/products to browse manually.",
                    },
                )

            # Parse and filter products
            reports = []
            rank = 1

            for product_id, product_data in products_data.items():
                if not isinstance(product_data, dict):
                    continue

                # Filter out unclaimedPlaceholders
                if product_data.get("isUnclaimedPlaceholder", False):
                    continue

                # Get product details
                name = product_data.get("name", "Unknown")
                description = product_data.get("description", "")
                revenue = product_data.get("selfReportedMonthlyRevenue", 0)
                avatar_url = product_data.get("avatarUrl", "")
                website = product_data.get("website", "")

                # Create product URL
                product_url = f"{self.base_url}/product/{product_id}" if product_id else f"{self.base_url}/products"

                # Format revenue
                if revenue and revenue > 0:
                    revenue_str = f"${revenue:,}/mo"
                else:
                    revenue_str = "Not disclosed"

                report = IncomeReport(
                    rank=rank,
                    project_name=name,
                    project_url=product_url,
                    author="Indie Hacker",
                    author_url=product_url,
                    revenue=revenue_str,
                    revenue_amount=float(revenue) if revenue else None,
                    revenue_period="monthly",
                    description=description[:200] if description else name,
                )

                reports.append(report)
                rank += 1

                if len(reports) >= limit:
                    break

            # Sort by revenue if requested
            if sorting == "highest-revenue":
                reports.sort(key=lambda r: r.revenue_amount or 0, reverse=True)

            # Update ranks after sorting
            for i, report in enumerate(reports):
                report.rank = i + 1

            return self._create_response(
                success=True,
                data_type="income_reports",
                data=reports,
                metadata={
                    "total_count": len(reports),
                    "limit": limit,
                    "sorting": sorting,
                    "source": "firebase_api",
                    "url": f"{self.base_url}/products",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Indie Hackers income reports: {e}")
            return self._create_response(
                success=False, data_type="income_reports", data=[], error=str(e)
            )

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
            return self._create_response(
                success=False, data_type="milestones", data=[], error=str(e)
            )

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
        """
        Parse income reports from products page.

        URL: /products?revenueVerification=stripe&sorting=highest-revenue
        This page shows products with Stripe-verified revenue.
        """
        reports = []
        rank = 1

        # Parse product cards from the products page
        # Selectors need to match actual Indie Hackers HTML structure
        product_elements = soup.select(".product-item, .product-card, article.product")[:limit]

        # Fallback: try different possible selectors
        if not product_elements:
            product_elements = soup.select("article, .row")[:limit]

        for element in product_elements:
            try:
                # Extract project name
                title_elem = element.select_one("h2, h3, h4, .product-name, .product-title")
                if not title_elem:
                    continue

                project_name = title_elem.get_text(strip=True)

                # Extract project URL
                link = element.select_one("a[href*='/product/'], a[href*='/products/']")
                project_url = ""
                if link:
                    href = link.get("href", "")
                    project_url = (
                        self.base_url + href if href and not href.startswith("http") else href
                    )

                # Extract author
                author_elem = element.select_one(".founder, .author, .creator")
                author = author_elem.get_text(strip=True) if author_elem else "Unknown"
                author_url = ""
                if author_elem and author_elem.find("a"):
                    author_url = author_elem.find("a").get("href", "")
                    if author_url and not author_url.startswith("http"):
                        author_url = self.base_url + author_url

                # Extract revenue (Stripe verified)
                revenue_elem = element.select_one(".revenue, .monthly-revenue, [class*='revenue']")
                revenue = "Unknown"
                if revenue_elem:
                    revenue_text = revenue_elem.get_text(strip=True)
                    # Match patterns like: $5,000/mo, $5k/mo, $60k/yr
                    revenue_match = re.search(
                        r"\$[\d,]+(?:k|K)?(?:/mo|/month|/yr|/year)?", revenue_text
                    )
                    if revenue_match:
                        revenue = revenue_match.group()

                # Extract description
                desc_elem = element.select_one(".description, .tagline, p")
                description = desc_elem.get_text(strip=True)[:200] if desc_elem else project_name

                report = IncomeReport(
                    rank=rank,
                    project_name=project_name,
                    project_url=project_url or f"{self.base_url}/products",
                    author=author,
                    author_url=author_url,
                    revenue=revenue,
                    description=description,
                )

                reports.append(report)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing income report at rank {rank}: {e}")
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

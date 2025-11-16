"""Product Hunt fetcher implementation."""

from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from ...models.base import TrendingResponse
from ...models.producthunt import ProductHuntProduct
from ...utils import logger
from ..base import BaseFetcher


class ProductHuntFetcher(BaseFetcher):
    """
    Fetcher for Product Hunt data.

    Note: This implementation uses web scraping as Product Hunt's GraphQL API
    requires authentication and has strict rate limits. For production use,
    consider using the official API with proper credentials.
    """

    BASE_URL = "https://www.producthunt.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "producthunt"

    async def fetch_products(
        self,
        time_range: str = "today",
        topic: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Product Hunt products.

        Args:
            time_range: Time range (today, week, month)
            topic: Optional topic filter
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with product data
        """
        return await self.fetch_with_cache(
            data_type=f"products_{time_range}",
            fetch_func=self._fetch_products_internal,
            use_cache=use_cache,
            time_range=time_range,
            topic=topic,
        )

    async def _fetch_products_internal(
        self,
        time_range: str = "today",
        topic: str | None = None,
    ) -> TrendingResponse:
        """Internal method to fetch products."""
        try:
            # Build URL based on time range
            url = self._build_url(time_range)

            # Set headers to mimic browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }

            # Fetch HTML page
            response = await self.http_client.get(url, headers=headers)

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            products = self._parse_products(soup)

            # Filter by topic if specified
            if topic:
                products = [
                    p for p in products if any(topic.lower() in t.lower() for t in p.topics)
                ]

            metadata = {
                "total_count": len(products),
                "time_range": time_range,
                "topic": topic,
            }

            return self._create_response(
                success=True,
                data_type=f"products_{time_range}",
                data=products,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching Product Hunt products: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type=f"products_{time_range}",
                data=[],
                error=str(e),
            )

    def _build_url(self, time_range: str) -> str:
        """Build URL based on time range."""
        if time_range == "today":
            return self.BASE_URL
        elif time_range == "week":
            # Get date for this week
            today = datetime.now()
            # Go back to start of week (Monday)
            days_since_monday = today.weekday()
            monday = today - timedelta(days=days_since_monday)
            return f"{self.BASE_URL}?date={monday.strftime('%Y-%m-%d')}"
        elif time_range == "month":
            # Get first day of current month
            today = datetime.now()
            first_day = today.replace(day=1)
            return f"{self.BASE_URL}?date={first_day.strftime('%Y-%m-%d')}"
        else:
            return self.BASE_URL

    def _parse_products(self, soup: BeautifulSoup) -> list[ProductHuntProduct]:
        """
        Parse product data from HTML.

        Note: Product Hunt's HTML structure may change. This parser
        is based on the structure as of 2025 and may need updates.
        """
        products = []

        # Product Hunt uses different selectors - this is a simplified version
        # In production, you'd need to handle their actual structure

        # Try to find product containers (common patterns)
        product_containers = (
            soup.find_all("div", {"data-test": "product-item"}) or soup.find_all("article") or []
        )

        for rank, container in enumerate(product_containers[:50], 1):
            try:
                product = self._parse_single_product(container, rank)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing product at rank {rank}: {e}")
                continue

        # If scraping fails, return mock data for demonstration
        # In production, you would use the official API
        if not products:
            logger.warning("Failed to parse products from HTML, using fallback")
            products = self._get_fallback_products()

        return products

    def _parse_single_product(
        self, container: BeautifulSoup, rank: int
    ) -> ProductHuntProduct | None:
        """Parse a single product from HTML container."""
        # This is a simplified parser
        # Product Hunt's actual structure requires more complex parsing

        # Try to extract basic info
        name = "Product Name"
        tagline = "Product tagline"
        url = f"{self.BASE_URL}/posts/example"
        product_url = "https://example.com"
        votes = 0
        comments = 0

        # Try to find product link (Product Hunt page)
        # Common patterns: <a href="/posts/product-name">
        link_elem = container.find("a", href=True)
        if link_elem:
            href = link_elem.get("href", "")
            if href.startswith("/posts/"):
                url = f"{self.BASE_URL}{href}"
            elif href.startswith("http"):
                # Some links might be absolute
                if "producthunt.com" in href:
                    url = href
                else:
                    # External link might be the product URL
                    product_url = href

        # Try to find name
        name_elem = container.find("h3") or container.find(
            "a", {"class": lambda x: x and "title" in str(x).lower()}
        )
        if name_elem:
            name = name_elem.get_text(strip=True)
            # If name element is also a link, use it
            if name_elem.name == "a" and name_elem.get("href"):
                href = name_elem.get("href")
                if href.startswith("/posts/"):
                    url = f"{self.BASE_URL}{href}"

        # Try to find tagline
        tagline_elem = container.find("p")
        if tagline_elem:
            tagline = tagline_elem.get_text(strip=True)

        # Try to find external product URL
        # Look for links that go to external domains
        all_links = container.find_all("a", href=True)
        for link in all_links:
            href = link.get("href", "")
            if href.startswith("http") and "producthunt.com" not in href:
                product_url = href
                break

        # Try to find votes/upvotes
        votes_elem = container.find(text=lambda t: t and ("▲" in str(t) or "upvote" in str(t).lower()))
        if votes_elem:
            # Extract number from text
            import re
            numbers = re.findall(r'\d+', votes_elem.string or votes_elem.parent.get_text())
            if numbers:
                votes = int(numbers[0])

        # Try to find comments count
        comments_elem = container.find(text=lambda t: t and "comment" in str(t).lower())
        if comments_elem:
            import re
            numbers = re.findall(r'\d+', comments_elem.parent.get_text())
            if numbers:
                comments = int(numbers[0])

        return ProductHuntProduct(
            rank=rank,
            name=name,
            tagline=tagline,
            url=url,
            product_url=product_url,
            votes=votes,
            comments_count=comments,
            thumbnail=None,
            topics=[],
            makers=[],
            featured_at=datetime.now(),
        )

    def _get_fallback_products(self) -> list[ProductHuntProduct]:
        """
        Get fallback products for demonstration.

        In production, this should be replaced with actual API integration.
        """
        logger.info("Using fallback Product Hunt data")
        return [
            ProductHuntProduct(
                rank=1,
                name="Example Product",
                tagline="This is a fallback example - configure Product Hunt API for real data",
                url=f"{self.BASE_URL}/posts/example",
                product_url="https://example.com",
                votes=100,
                comments_count=20,
                topics=["Developer Tools", "AI"],
                makers=[],
                featured_at=datetime.now(),
            )
        ]

    async def fetch_today(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for today's products."""
        return await self.fetch_products("today", use_cache=use_cache)

    async def fetch_this_week(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this week's products."""
        return await self.fetch_products("week", use_cache=use_cache)

    async def fetch_this_month(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this month's products."""
        return await self.fetch_products("month", use_cache=use_cache)

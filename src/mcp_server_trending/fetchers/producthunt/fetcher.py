"""Product Hunt fetcher implementation using RSS feed."""

import re
from datetime import datetime, timedelta, timezone

from ...models.base import TrendingResponse
from ...models.producthunt import ProductHuntProduct
from ...utils import logger
from ..base import BaseFetcher


class ProductHuntFetcher(BaseFetcher):
    """
    Fetcher for Product Hunt data using public RSS feed.

    No authentication required! Uses Product Hunt's public RSS feed.

    Features:
    - Product name, tagline, description
    - Author/maker information
    - Published date
    - Product link

    Limitations (RSS doesn't provide):
    - Vote counts
    - Comment counts
    - Topics/tags
    - Thumbnails
    """

    BASE_URL = "https://www.producthunt.com"
    RSS_URL = "https://www.producthunt.com/feed"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "producthunt"

    def _parse_time_range(self, time_range: str) -> timedelta:
        """
        Parse time range string to timedelta.

        Supports:
        - "today" or "1day" -> 1 day
        - "week" or "7days" -> 7 days
        - "month" or "30days" -> 30 days
        - "3days" -> 3 days
        - "2weeks" -> 14 days

        Args:
            time_range: Time range string

        Returns:
            timedelta object
        """
        # Normalize to lowercase
        time_range = time_range.lower().strip()

        # Pre-defined mappings
        mappings = {
            "today": timedelta(days=1),
            "week": timedelta(days=7),
            "month": timedelta(days=30),
        }

        if time_range in mappings:
            return mappings[time_range]

        # Parse patterns like "3days", "2weeks", "1month"
        # Match: number + (day|days|week|weeks|month|months)
        match = re.match(r"(\d+)\s*(day|days|week|weeks|month|months)", time_range)
        if match:
            num = int(match.group(1))
            unit = match.group(2)

            if "day" in unit:
                return timedelta(days=num)
            elif "week" in unit:
                return timedelta(weeks=num)
            elif "month" in unit:
                return timedelta(days=num * 30)

        # Default to 1 day
        logger.warning(f"Unknown time range '{time_range}', defaulting to 1 day")
        return timedelta(days=1)

    async def fetch_products(
        self,
        time_range: str = "today",
        topic: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Product Hunt products using RSS feed.

        Args:
            time_range: Time range filter
                - "today", "1day" -> last 24 hours
                - "week", "7days" -> last 7 days
                - "month", "30days" -> last 30 days
                - Custom: "3days", "2weeks", etc.
            topic: Optional topic filter (not supported by RSS)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with product data
        """
        return await self.fetch_with_cache(
            data_type=f"products_{time_range}",
            fetch_func=self._fetch_products_from_rss,
            use_cache=use_cache,
            time_range=time_range,
            topic=topic,
        )

    async def _fetch_products_from_rss(
        self,
        time_range: str = "today",
        topic: str | None = None,
    ) -> TrendingResponse:
        """
        Fetch products from Product Hunt RSS feed.

        Args:
            time_range: Time range filter
            topic: Optional topic filter (not supported)

        Returns:
            TrendingResponse with product data
        """
        try:
            import xml.etree.ElementTree as ET

            # Parse time range
            time_delta = self._parse_time_range(time_range)
            cutoff = datetime.now(timezone.utc) - time_delta

            logger.info(f"Fetching Product Hunt products from RSS (time_range={time_range}, cutoff={cutoff.strftime('%Y-%m-%d %H:%M')})")

            response = await self.http_client.get(
                self.RSS_URL,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entries = root.findall('atom:entry', ns)
            products = []

            for entry in entries:
                try:
                    # Parse published date first
                    published_elem = entry.find('atom:published', ns)
                    if published_elem is None or not published_elem.text:
                        continue

                    published_text = published_elem.text
                    published_date = datetime.fromisoformat(
                        published_text.replace('Z', '+00:00')
                    )

                    # Filter by time range
                    if published_date < cutoff:
                        continue

                    # Extract product info
                    title_elem = entry.find('atom:title', ns)
                    link_elem = entry.find('atom:link[@rel="alternate"]', ns)
                    content_elem = entry.find('atom:content', ns)
                    author_elem = entry.find('atom:author/atom:name', ns)

                    title = title_elem.text.strip() if title_elem is not None else "Unknown"
                    url = link_elem.get('href') if link_elem is not None else ""

                    # Extract tagline from content
                    tagline = ""
                    if content_elem is not None and content_elem.text:
                        # Parse HTML content to extract tagline
                        content_html = content_elem.text
                        # Extract text between <p> tags
                        match = re.search(r'<p>\s*([^<]+)\s*</p>', content_html)
                        if match:
                            tagline = match.group(1).strip()

                    author = author_elem.text if author_elem is not None else "Unknown"

                    product = ProductHuntProduct(
                        rank=len(products) + 1,
                        name=title,
                        tagline=tagline,
                        description=tagline,  # RSS doesn't have full description
                        url=url,
                        product_url=url,
                        votes=0,  # RSS doesn't include vote count
                        comments_count=0,  # RSS doesn't include comment count
                        thumbnail=None,  # RSS doesn't include thumbnails
                        topics=[],  # RSS doesn't include topics
                        makers=[author] if author != "Unknown" else [],
                        featured_at=published_date,
                    )

                    products.append(product)

                    # Limit to 20 products
                    if len(products) >= 20:
                        break

                except Exception as e:
                    logger.warning(f"Error parsing RSS entry: {e}")
                    continue

            logger.info(f"Successfully fetched {len(products)} products from RSS feed (time_range={time_range})")

            return self._create_response(
                success=True,
                data_type=f"products_{time_range}",
                data=products,
                metadata={
                    "total_count": len(products),
                    "time_range": time_range,
                    "time_delta_days": time_delta.days,
                    "source": "rss_feed",
                    "note": f"Using RSS feed (no authentication required). Showing products from the last {time_range}.",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching from RSS feed: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type=f"products_{time_range}",
                data=[],
                error=str(e),
            )

    async def fetch_today(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for today's products."""
        return await self.fetch_products("today", use_cache=use_cache)

    async def fetch_this_week(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this week's products."""
        return await self.fetch_products("week", use_cache=use_cache)

    async def fetch_this_month(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this month's products."""
        return await self.fetch_products("month", use_cache=use_cache)

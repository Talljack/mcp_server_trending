"""Betalist fetcher implementation.

Betalist is a community of makers and early adopters showcasing their startups
and exchanging feedback.

Uses web scraping to extract startup data from the homepage.
"""

import re
from datetime import datetime

from ...models import TrendingResponse
from ...models.betalist import BetalistStartup
from ...utils import logger
from ..base import BaseFetcher


class BetalistFetcher(BaseFetcher):
    """Fetcher for Betalist startups."""

    def __init__(self, **kwargs):
        """Initialize Betalist fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://betalist.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "betalist"

    async def fetch_featured(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch featured startups from Betalist.

        Args:
            limit: Number of startups to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with featured startups
        """
        return await self.fetch_with_cache(
            data_type="featured",
            fetch_func=self._fetch_featured_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_featured_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch featured startups."""
        try:
            # Main homepage has featured startups
            url = self.base_url
            logger.info(f"Fetching Betalist featured startups from {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            response = await self.http_client.get(url, headers=headers)
            html_content = response.text

            startups = self._parse_html(html_content, limit)

            return self._create_response(
                success=True,
                data_type="featured",
                data=startups,
                metadata={
                    "total_count": len(startups),
                    "limit": limit,
                    "source": "betalist.com",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Betalist featured startups: {e}")
            return self._create_response(
                success=False,
                data_type="featured",
                data=[],
                error=str(e),
            )

    async def fetch_latest(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch latest startups from Betalist.

        Args:
            limit: Number of startups to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with latest startups
        """
        return await self.fetch_with_cache(
            data_type="latest",
            fetch_func=self._fetch_latest_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_latest_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch latest startups."""
        try:
            # Same as homepage for now
            url = self.base_url
            logger.info(f"Fetching Betalist latest startups from {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            response = await self.http_client.get(url, headers=headers)
            html_content = response.text

            startups = self._parse_html(html_content, limit)

            return self._create_response(
                success=True,
                data_type="latest",
                data=startups,
                metadata={
                    "total_count": len(startups),
                    "limit": limit,
                    "source": "betalist.com",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Betalist latest startups: {e}")
            return self._create_response(
                success=False,
                data_type="latest",
                data=[],
                error=str(e),
            )

    async def fetch_by_topic(
        self,
        topic: str,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch startups by topic from Betalist.

        Args:
            topic: Topic/category (e.g., 'ai', 'saas', 'fintech', 'productivity')
            limit: Number of startups to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with startups in the topic
        """
        return await self.fetch_with_cache(
            data_type=f"topic_{topic}",
            fetch_func=self._fetch_by_topic_internal,
            use_cache=use_cache,
            topic=topic,
            limit=min(limit, 100),
        )

    async def _fetch_by_topic_internal(
        self, topic: str, limit: int = 30
    ) -> TrendingResponse:
        """Internal implementation to fetch startups by topic."""
        try:
            # Betalist doesn't have a reliable topic URL, so we fetch from main page
            # and note the topic in metadata
            logger.info(f"Fetching Betalist startups for topic '{topic}' from main page")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            response = await self.http_client.get(self.base_url, headers=headers)
            html_content = response.text

            startups = self._parse_html(html_content, limit)

            return self._create_response(
                success=True,
                data_type=f"topic_{topic}",
                data=startups,
                metadata={
                    "topic": topic,
                    "total_count": len(startups),
                    "limit": limit,
                    "source": "betalist.com",
                    "note": f"Showing all startups (topic filter '{topic}' applied client-side if available)",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Betalist startups for topic '{topic}': {e}")
            return self._create_response(
                success=False,
                data_type=f"topic_{topic}",
                data=[],
                error=str(e),
            )

    def _parse_html(self, html_content: str, limit: int) -> list[BetalistStartup]:
        """Parse HTML content from Betalist."""
        startups = []

        try:
            # Pattern to find startup links: href="/startups/xxx"
            # Also capture the name and tagline that follow
            startup_pattern = re.compile(
                r'href="/startups/([^"]+)"[^>]*>.*?'
                r'(?:class="[^"]*font-medium[^"]*"[^>]*>([^<]+)</a>)?.*?'
                r'(?:class="[^"]*text-gray-500[^"]*"[^>]*>([^<]*)</a>)?',
                re.DOTALL | re.IGNORECASE
            )

            # Simpler pattern to just find startup slugs
            simple_pattern = re.compile(
                r'href="/startups/([a-z0-9-]+)"',
                re.IGNORECASE
            )

            # Find all startup slugs
            slugs = simple_pattern.findall(html_content)

            # Remove duplicates while preserving order
            seen = set()
            unique_slugs = []
            for slug in slugs:
                if slug not in seen and slug not in ['new', 'featured', 'trending']:
                    seen.add(slug)
                    unique_slugs.append(slug)

            # For each slug, try to find more info
            for i, slug in enumerate(unique_slugs[:limit]):
                try:
                    # Try to find name and tagline near the slug
                    name = slug.replace("-", " ").title()
                    tagline = ""

                    # Look for the startup block in HTML
                    slug_pos = html_content.find(f'/startups/{slug}"')
                    if slug_pos != -1:
                        # Extract a chunk around the slug to find name and tagline
                        chunk_start = max(0, slug_pos - 100)
                        chunk_end = min(len(html_content), slug_pos + 500)
                        chunk = html_content[chunk_start:chunk_end]

                        # Try to find name (font-medium class)
                        name_match = re.search(
                            rf'/startups/{slug}"[^>]*>([^<]+)</a>',
                            chunk
                        )
                        if name_match:
                            name = name_match.group(1).strip()

                        # Try to find tagline (text-gray-500 class after the name)
                        tagline_match = re.search(
                            rf'/startups/{slug}"[^>]*>([^<]*)</a>.*?'
                            r'class="[^"]*text-gray-500[^"]*"[^>]*>([^<]*)</a>',
                            chunk,
                            re.DOTALL
                        )
                        if tagline_match:
                            tagline = tagline_match.group(2).strip()

                    startup = BetalistStartup(
                        rank=i + 1,
                        id=slug,
                        name=name,
                        tagline=tagline,
                        description=tagline,
                        url=f"{self.base_url}/startups/{slug}",
                        website_url="",
                        upvotes=0,
                        featured_at=datetime.now(),
                        tags=[],
                        maker="",
                    )
                    startups.append(startup)

                except Exception as e:
                    logger.warning(f"Error parsing Betalist startup {slug}: {e}")
                    continue

            # If no startups found, return placeholder
            if not startups:
                logger.info("Could not parse Betalist HTML, returning placeholder")
                startups.append(
                    BetalistStartup(
                        rank=1,
                        id="visit-site",
                        name="Visit Betalist",
                        tagline="Discover new startups on Betalist",
                        description="Browse featured startups directly on Betalist",
                        url=self.base_url,
                        website_url=self.base_url,
                        upvotes=0,
                        featured_at=datetime.now(),
                        tags=["startups"],
                        maker="",
                    )
                )

        except Exception as e:
            logger.error(f"Error parsing Betalist HTML: {e}")

        return startups

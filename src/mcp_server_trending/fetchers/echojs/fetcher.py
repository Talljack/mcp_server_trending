"""Echo JS fetcher implementation.

Echo JS is a community-driven news site entirely focused on JavaScript development,
HTML5, and front-end news.

API: https://www.echojs.com/api/
- Public API, no authentication required
- Endpoints: /api/getnews/latest/0/30, /api/getnews/top/0/30
"""

from datetime import datetime

from ...models import TrendingResponse
from ...models.echojs import EchoJSNews
from ...utils import logger
from ..base import BaseFetcher


class EchoJSFetcher(BaseFetcher):
    """Fetcher for Echo JS news."""

    def __init__(self, **kwargs):
        """Initialize Echo JS fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://www.echojs.com"
        self.api_url = "https://www.echojs.com/api"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "echojs"

    async def fetch_latest(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch latest news from Echo JS.

        Args:
            limit: Number of news items to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with latest news
        """
        return await self.fetch_with_cache(
            data_type="latest",
            fetch_func=self._fetch_latest_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_latest_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch latest news."""
        try:
            # Echo JS API uses start/count format
            url = f"{self.api_url}/getnews/latest/0/{limit}"
            logger.info(f"Fetching Echo JS latest news from {url}")

            response = await self.http_client.get(url)
            data = response.json()

            news_items = self._parse_news(data.get("news", []), limit)

            return self._create_response(
                success=True,
                data_type="latest",
                data=news_items,
                metadata={
                    "total_count": len(news_items),
                    "limit": limit,
                    "source": "echojs.com",
                    "sort": "latest",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Echo JS latest news: {e}")
            return self._create_response(
                success=False,
                data_type="latest",
                data=[],
                error=str(e),
            )

    async def fetch_top(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch top/trending news from Echo JS.

        Args:
            limit: Number of news items to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with top news
        """
        return await self.fetch_with_cache(
            data_type="top",
            fetch_func=self._fetch_top_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_top_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch top news."""
        try:
            url = f"{self.api_url}/getnews/top/0/{limit}"
            logger.info(f"Fetching Echo JS top news from {url}")

            response = await self.http_client.get(url)
            data = response.json()

            news_items = self._parse_news(data.get("news", []), limit)

            return self._create_response(
                success=True,
                data_type="top",
                data=news_items,
                metadata={
                    "total_count": len(news_items),
                    "limit": limit,
                    "source": "echojs.com",
                    "sort": "top",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Echo JS top news: {e}")
            return self._create_response(
                success=False,
                data_type="top",
                data=[],
                error=str(e),
            )

    def _parse_news(self, data: list, limit: int) -> list[EchoJSNews]:
        """Parse news items from Echo JS API response."""
        news_items = []

        for i, item in enumerate(data[:limit]):
            try:
                # Parse creation timestamp
                ctime = item.get("ctime", 0)
                try:
                    created_at = datetime.fromtimestamp(int(ctime))
                except (ValueError, TypeError):
                    created_at = datetime.now()

                news = EchoJSNews(
                    rank=i + 1,
                    id=item.get("id", ""),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    created_at=created_at,
                    up=int(item.get("up", 0) or 0),
                    down=int(item.get("down", 0) or 0),
                    comments=int(item.get("comments", 0) or 0),
                    username=item.get("username", ""),
                    ctime=int(ctime) if ctime else 0,
                )
                news_items.append(news)

            except Exception as e:
                logger.warning(f"Error parsing Echo JS news item: {e}")
                continue

        return news_items

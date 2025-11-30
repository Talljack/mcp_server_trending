"""Lobsters fetcher implementation.

Lobsters is a computing-focused community centered around link aggregation and discussion.
Similar to Hacker News but with a focus on high-quality technical content.

API Documentation: https://lobste.rs/about
- Public JSON API, no authentication required
- Rate limiting: Be reasonable (no explicit limits)
"""

from datetime import datetime

from ...models import TrendingResponse
from ...models.lobsters import LobstersStory
from ...utils import logger
from ..base import BaseFetcher


class LobstersFetcher(BaseFetcher):
    """Fetcher for Lobsters stories."""

    def __init__(self, **kwargs):
        """Initialize Lobsters fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://lobste.rs"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "lobsters"

    async def fetch_hottest(
        self,
        limit: int = 25,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch hottest stories from Lobsters.

        Args:
            limit: Number of stories to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with hottest stories
        """
        return await self.fetch_with_cache(
            data_type="hottest",
            fetch_func=self._fetch_hottest_internal,
            use_cache=use_cache,
            limit=min(limit, 50),
        )

    async def _fetch_hottest_internal(self, limit: int = 25) -> TrendingResponse:
        """Internal implementation to fetch hottest stories."""
        try:
            url = f"{self.base_url}/hottest.json"
            logger.info(f"Fetching Lobsters hottest stories from {url}")

            response = await self.http_client.get(url)
            data = response.json()

            stories = self._parse_stories(data, limit)

            return self._create_response(
                success=True,
                data_type="hottest",
                data=stories,
                metadata={
                    "total_count": len(stories),
                    "limit": limit,
                    "source": "lobste.rs",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Lobsters hottest stories: {e}")
            return self._create_response(
                success=False,
                data_type="hottest",
                data=[],
                error=str(e),
            )

    async def fetch_newest(
        self,
        limit: int = 25,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch newest stories from Lobsters.

        Args:
            limit: Number of stories to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with newest stories
        """
        return await self.fetch_with_cache(
            data_type="newest",
            fetch_func=self._fetch_newest_internal,
            use_cache=use_cache,
            limit=min(limit, 50),
        )

    async def _fetch_newest_internal(self, limit: int = 25) -> TrendingResponse:
        """Internal implementation to fetch newest stories."""
        try:
            url = f"{self.base_url}/newest.json"
            logger.info(f"Fetching Lobsters newest stories from {url}")

            response = await self.http_client.get(url)
            data = response.json()

            stories = self._parse_stories(data, limit)

            return self._create_response(
                success=True,
                data_type="newest",
                data=stories,
                metadata={
                    "total_count": len(stories),
                    "limit": limit,
                    "source": "lobste.rs",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Lobsters newest stories: {e}")
            return self._create_response(
                success=False,
                data_type="newest",
                data=[],
                error=str(e),
            )

    async def fetch_by_tag(
        self,
        tag: str,
        limit: int = 25,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch stories by tag from Lobsters.

        Args:
            tag: Tag to filter by (e.g., 'python', 'javascript', 'ai')
            limit: Number of stories to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with stories for the tag
        """
        return await self.fetch_with_cache(
            data_type=f"tag_{tag}",
            fetch_func=self._fetch_by_tag_internal,
            use_cache=use_cache,
            tag=tag,
            limit=min(limit, 50),
        )

    async def _fetch_by_tag_internal(self, tag: str, limit: int = 25) -> TrendingResponse:
        """Internal implementation to fetch stories by tag."""
        try:
            url = f"{self.base_url}/t/{tag}.json"
            logger.info(f"Fetching Lobsters stories for tag '{tag}' from {url}")

            response = await self.http_client.get(url)
            data = response.json()

            stories = self._parse_stories(data, limit)

            return self._create_response(
                success=True,
                data_type=f"tag_{tag}",
                data=stories,
                metadata={
                    "tag": tag,
                    "total_count": len(stories),
                    "limit": limit,
                    "source": "lobste.rs",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Lobsters stories for tag '{tag}': {e}")
            return self._create_response(
                success=False,
                data_type=f"tag_{tag}",
                data=[],
                error=str(e),
            )

    def _parse_stories(self, data: list, limit: int) -> list[LobstersStory]:
        """Parse stories from Lobsters API response."""
        stories = []

        for i, item in enumerate(data[:limit]):
            try:
                # Parse created_at timestamp
                created_at_str = item.get("created_at", "")
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    created_at = datetime.now()

                # submitter_user can be a string or dict depending on API endpoint
                submitter = item.get("submitter_user", "")
                if isinstance(submitter, dict):
                    submitter = submitter.get("username", "")

                story = LobstersStory(
                    rank=i + 1,
                    short_id=item.get("short_id", ""),
                    title=item.get("title", ""),
                    url=item.get("url", "") or f"{self.base_url}/s/{item.get('short_id', '')}",
                    created_at=created_at,
                    score=item.get("score", 0),
                    upvotes=item.get("upvotes", 0),
                    downvotes=item.get("downvotes", 0),
                    comment_count=item.get("comment_count", 0),
                    description=item.get("description", "") or item.get("description_plain", "") or "",
                    submitter_user=submitter,
                    user_is_author=item.get("user_is_author", False),
                    tags=item.get("tags", []),
                    comments_url=item.get("comments_url", "") or f"{self.base_url}/s/{item.get('short_id', '')}",
                )
                stories.append(story)

            except Exception as e:
                logger.warning(f"Error parsing Lobsters story: {e}")
                continue

        return stories

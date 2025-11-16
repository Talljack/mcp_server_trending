"""Hacker News fetcher implementation."""

import asyncio
from datetime import datetime

from ...models.base import TrendingResponse
from ...models.hackernews import HackerNewsStory
from ...utils import logger
from ..base import BaseFetcher


class HackerNewsFetcher(BaseFetcher):
    """Fetcher for Hacker News data using official Firebase API."""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "hackernews"

    async def fetch_stories(
        self,
        story_type: str = "top",
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Hacker News stories.

        Args:
            story_type: Type of stories (top, best, new, ask, show, job)
            limit: Number of stories to fetch (max 500)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with story data
        """
        return await self.fetch_with_cache(
            data_type=f"stories_{story_type}",
            fetch_func=self._fetch_stories_internal,
            use_cache=use_cache,
            story_type=story_type,
            limit=limit,
        )

    async def _fetch_stories_internal(
        self,
        story_type: str = "top",
        limit: int = 30,
    ) -> TrendingResponse:
        """Internal method to fetch stories."""
        try:
            # Validate story type
            valid_types = ["top", "best", "new", "ask", "show", "job"]
            if story_type not in valid_types:
                raise ValueError(f"Invalid story_type: {story_type}. Must be one of {valid_types}")

            # Limit to reasonable range
            limit = min(max(1, limit), 500)

            # Fetch story IDs
            story_ids_url = f"{self.BASE_URL}/{story_type}stories.json"
            story_ids_response = await self.http_client.get(story_ids_url)
            story_ids = story_ids_response.json()[:limit]

            logger.info(f"Fetching {len(story_ids)} {story_type} stories from Hacker News")

            # Fetch story details in parallel
            stories = await self._fetch_story_details(story_ids)

            # Add rank
            for rank, story in enumerate(stories, 1):
                story.rank = rank

            metadata = {
                "total_count": len(stories),
                "story_type": story_type,
                "limit": limit,
            }

            return self._create_response(
                success=True,
                data_type=f"stories_{story_type}",
                data=stories,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching Hacker News stories: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type=f"stories_{story_type}",
                data=[],
                error=str(e),
            )

    async def _fetch_story_details(self, story_ids: list[int]) -> list[HackerNewsStory]:
        """
        Fetch details for multiple stories in parallel.

        Args:
            story_ids: List of story IDs

        Returns:
            List of HackerNewsStory objects
        """
        # Fetch stories in parallel with concurrency limit
        semaphore = asyncio.Semaphore(10)  # Limit concurrent requests

        async def fetch_one(story_id: int) -> HackerNewsStory:
            async with semaphore:
                try:
                    url = f"{self.BASE_URL}/item/{story_id}.json"
                    response = await self.http_client.get(url)
                    data = response.json()
                    return self._parse_story(data)
                except Exception as e:
                    logger.warning(f"Error fetching story {story_id}: {e}")
                    return None

        tasks = [fetch_one(story_id) for story_id in story_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out None and exceptions
        stories = [story for story in results if isinstance(story, HackerNewsStory)]

        return stories

    def _parse_story(self, data: dict) -> HackerNewsStory:
        """Parse story data from API response."""
        # Determine story type
        story_type = data.get("type", "story")

        # URL (may be None for Ask HN, etc.)
        url = data.get("url")

        # If no URL, generate HN link
        if not url:
            url = f"https://news.ycombinator.com/item?id={data.get('id')}"

        return HackerNewsStory(
            rank=0,  # Will be set later
            id=data.get("id", 0),
            title=data.get("title", ""),
            url=url,
            score=data.get("score", 0),
            author=data.get("by", "unknown"),
            time=datetime.fromtimestamp(data.get("time", 0)),
            descendants=data.get("descendants", 0),
            story_type=story_type,
        )

    async def fetch_top_stories(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """Convenience method for top stories."""
        return await self.fetch_stories("top", limit, use_cache)

    async def fetch_best_stories(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """Convenience method for best stories."""
        return await self.fetch_stories("best", limit, use_cache)

    async def fetch_ask_stories(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """Convenience method for Ask HN stories."""
        return await self.fetch_stories("ask", limit, use_cache)

    async def fetch_show_stories(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """Convenience method for Show HN stories."""
        return await self.fetch_stories("show", limit, use_cache)

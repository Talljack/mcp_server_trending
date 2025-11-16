"""V2EX fetcher implementation."""

from datetime import datetime
from typing import Any

from ...models import TrendingResponse, V2EXTopic
from ...utils import logger
from ..base import BaseFetcher


class V2EXFetcher(BaseFetcher):
    """Fetcher for V2EX topics."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://www.v2ex.com/api"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "v2ex"

    async def fetch_hot_topics(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch hot topics from V2EX.

        Args:
            limit: Maximum number of topics to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with V2EX topics
        """
        cache_key = f"hot_topics:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_hot_topics_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_hot_topics_internal(self, limit: int = 20) -> TrendingResponse:
        """Internal implementation to fetch hot topics."""
        try:
            url = f"{self.base_url}/topics/hot.json"

            logger.info(f"Fetching V2EX hot topics (limit={limit})")

            response = await self.http_client.get(url)
            data = response.json()

            topics = self._parse_topics(data, limit)

            return self._create_response(
                success=True,
                data_type="hot_topics",
                data=topics,
                metadata={
                    "total_count": len(topics),
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching V2EX hot topics: {e}")
            return self._create_response(
                success=False, data_type="hot_topics", data=[], error=str(e)
            )

    async def fetch_latest_topics(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch latest topics from V2EX.

        Args:
            limit: Maximum number of topics to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with V2EX topics
        """
        cache_key = f"latest_topics:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_latest_topics_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_latest_topics_internal(self, limit: int = 20) -> TrendingResponse:
        """Internal implementation to fetch latest topics."""
        try:
            url = f"{self.base_url}/topics/latest.json"

            logger.info(f"Fetching V2EX latest topics (limit={limit})")

            response = await self.http_client.get(url)
            data = response.json()

            topics = self._parse_topics(data, limit)

            return self._create_response(
                success=True,
                data_type="latest_topics",
                data=topics,
                metadata={
                    "total_count": len(topics),
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching V2EX latest topics: {e}")
            return self._create_response(
                success=False, data_type="latest_topics", data=[], error=str(e)
            )

    def _parse_topics(self, topics_data: list[dict[str, Any]], limit: int = 20) -> list[V2EXTopic]:
        """Parse topics from V2EX API response."""
        topics = []
        rank = 1

        for topic_data in topics_data[:limit]:
            try:
                # Parse timestamps
                created = None
                if "created" in topic_data:
                    try:
                        created = datetime.fromtimestamp(topic_data["created"])
                    except (ValueError, TypeError):
                        pass

                last_modified = None
                if "last_modified" in topic_data:
                    try:
                        last_modified = datetime.fromtimestamp(topic_data["last_modified"])
                    except (ValueError, TypeError):
                        pass

                last_reply_time = None
                if "last_reply_time" in topic_data and topic_data["last_reply_time"]:
                    try:
                        last_reply_time = datetime.fromtimestamp(topic_data["last_reply_time"])
                    except (ValueError, TypeError):
                        pass

                topic = V2EXTopic(
                    rank=rank,
                    id=topic_data.get("id", 0),
                    title=topic_data.get("title", ""),
                    url=topic_data.get("url", f"https://www.v2ex.com/t/{topic_data.get('id')}"),
                    content=topic_data.get("content"),
                    content_rendered=topic_data.get("content_rendered"),
                    member_id=topic_data.get("member", {}).get("id"),
                    member_username=topic_data.get("member", {}).get("username"),
                    member_avatar=topic_data.get("member", {}).get("avatar_large"),
                    node_id=topic_data.get("node", {}).get("id"),
                    node_name=topic_data.get("node", {}).get("name"),
                    node_title=topic_data.get("node", {}).get("title"),
                    replies=topic_data.get("replies", 0),
                    last_reply_time=last_reply_time,
                    created=created,
                    last_modified=last_modified,
                )

                topics.append(topic)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing V2EX topic: {e}")
                continue

        return topics

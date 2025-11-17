"""Stack Overflow fetcher implementation."""

from datetime import datetime

from ...models.base import TrendingResponse
from ...models.stackoverflow import StackOverflowTag
from ...utils import logger
from ..base import BaseFetcher


class StackOverflowFetcher(BaseFetcher):
    """Fetcher for Stack Overflow tags using Stack Exchange API."""

    BASE_URL = "https://api.stackexchange.com/2.3"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "stackoverflow"

    async def fetch_tags(
        self,
        sort: str = "popular",
        order: str = "desc",
        limit: int = 30,
        site: str = "stackoverflow",
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Stack Overflow tags.

        Args:
            sort: Sort order (popular, activity, name)
            order: Sort direction (desc, asc)
            limit: Number of tags to fetch (max 100)
            site: Site name (default: stackoverflow)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with tag data
        """
        return await self.fetch_with_cache(
            data_type=f"tags_{sort}_{order}",
            fetch_func=self._fetch_tags_internal,
            use_cache=use_cache,
            sort=sort,
            order=order,
            limit=min(limit, 100),
            site=site,
        )

    async def _fetch_tags_internal(
        self,
        sort: str = "popular",
        order: str = "desc",
        limit: int = 30,
        site: str = "stackoverflow",
    ) -> TrendingResponse:
        """Internal implementation to fetch tags."""
        try:
            url = f"{self.BASE_URL}/tags"
            params = {
                "order": order,
                "sort": sort,
                "site": site,
                "pagesize": min(limit, 100),
                "filter": "default",  # Get basic fields
            }

            logger.info(f"Fetching Stack Overflow tags (sort={sort}, order={order}, limit={limit})")
            response = await self.http_client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"Stack Exchange API returned status {response.status_code}")
                return self._create_response(
                    success=False,
                    data_type="tags",
                    data=[],
                    error=f"HTTP {response.status_code}",
                )

            data = response.json()

            if "items" not in data:
                logger.warning("No items in Stack Exchange API response")
                return self._create_response(
                    success=True,
                    data_type="tags",
                    data=[],
                    metadata={
                        "total_count": 0,
                        "limit": limit,
                        "quota_remaining": data.get("quota_remaining", 0),
                    },
                )

            tags_data = data["items"]
            tags = []

            for i, tag_data in enumerate(tags_data, 1):
                # Parse last activity date
                last_activity_date = None
                if "last_activity_date" in tag_data and tag_data["last_activity_date"]:
                    try:
                        last_activity_date = datetime.fromtimestamp(tag_data["last_activity_date"])
                    except (ValueError, TypeError, OSError):
                        pass

                tag = StackOverflowTag(
                    rank=i,
                    name=tag_data.get("name", ""),
                    count=tag_data.get("count", 0),
                    has_synonyms=tag_data.get("has_synonyms", False),
                    is_moderator_only=tag_data.get("is_moderator_only", False),
                    is_required=tag_data.get("is_required", False),
                    url=f"https://stackoverflow.com/tags/{tag_data.get('name', '')}",
                    last_activity_date=last_activity_date,
                )

                tags.append(tag)

            return self._create_response(
                success=True,
                data_type="tags",
                data=tags,
                metadata={
                    "total_count": len(tags),
                    "limit": limit,
                    "sort": sort,
                    "order": order,
                    "site": site,
                    "quota_remaining": data.get("quota_remaining", 0),
                    "has_more": data.get("has_more", False),
                    "url": f"https://stackoverflow.com/tags?tab={sort}",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Stack Overflow tags: {e}")
            return self._create_response(
                success=False, data_type="tags", data=[], error=str(e)
            )


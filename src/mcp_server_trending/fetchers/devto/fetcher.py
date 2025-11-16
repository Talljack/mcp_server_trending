"""dev.to fetcher implementation."""

from datetime import datetime
from typing import Any

from ...models import DevToArticle, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class DevToFetcher(BaseFetcher):
    """Fetcher for dev.to articles."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://dev.to/api"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "devto"

    async def fetch_articles(
        self,
        per_page: int = 30,
        page: int = 1,
        tag: str | None = None,
        top: int | None = None,  # Number for top articles (e.g., 7 for weekly)
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch articles from dev.to.

        Args:
            per_page: Number of articles per page (max 1000)
            page: Page number
            tag: Filter by tag
            top: Number for top articles (1=daily, 7=weekly, 30=monthly, 365=yearly)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with dev.to articles
        """
        cache_key = f"articles:page={page}:per_page={per_page}:tag={tag}:top={top}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_articles_internal,
            use_cache=use_cache,
            per_page=per_page,
            page=page,
            tag=tag,
            top=top,
        )

    async def _fetch_articles_internal(
        self,
        per_page: int = 30,
        page: int = 1,
        tag: str | None = None,
        top: int | None = None,
    ) -> TrendingResponse:
        """Internal implementation to fetch articles."""
        try:
            url = f"{self.base_url}/articles"
            params = {
                "per_page": min(per_page, 1000),
                "page": page,
            }

            if tag:
                params["tag"] = tag
            if top:
                params["top"] = top

            logger.info(f"Fetching dev.to articles (per_page={per_page}, tag={tag}, top={top})")

            response = await self.http_client.get(url, params=params)
            data = response.json()

            articles = self._parse_articles(data)

            return self._create_response(
                success=True,
                data_type="articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "per_page": per_page,
                    "page": page,
                    "tag": tag,
                    "top": top,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching dev.to articles: {e}")
            return self._create_response(success=False, data_type="articles", data=[], error=str(e))

    def _parse_articles(self, articles_data: list[dict[str, Any]]) -> list[DevToArticle]:
        """Parse articles from dev.to API response."""
        articles = []
        rank = 1

        for article_data in articles_data:
            try:
                # Parse timestamps
                published_at = None
                if "published_at" in article_data and article_data["published_at"]:
                    try:
                        published_at = datetime.fromisoformat(
                            article_data["published_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                created_at = None
                if "created_at" in article_data and article_data["created_at"]:
                    try:
                        created_at = datetime.fromisoformat(
                            article_data["created_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                edited_at = None
                if "edited_at" in article_data and article_data["edited_at"]:
                    try:
                        edited_at = datetime.fromisoformat(
                            article_data["edited_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                last_comment_at = None
                if "last_comment_at" in article_data and article_data["last_comment_at"]:
                    try:
                        last_comment_at = datetime.fromisoformat(
                            article_data["last_comment_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                # Extract user info
                user_data = article_data.get("user", {})

                # Extract organization info
                org_data = article_data.get("organization", {})

                article = DevToArticle(
                    rank=rank,
                    id=article_data.get("id", 0),
                    title=article_data.get("title", ""),
                    url=article_data.get("url", ""),
                    description=article_data.get("description"),
                    cover_image=article_data.get("cover_image"),
                    user_id=user_data.get("user_id") if user_data else None,
                    user_name=user_data.get("name") if user_data else None,
                    user_username=user_data.get("username") if user_data else None,
                    user_profile_image=user_data.get("profile_image") if user_data else None,
                    organization_id=org_data.get("organization_id") if org_data else None,
                    organization_name=org_data.get("name") if org_data else None,
                    organization_username=org_data.get("username") if org_data else None,
                    tags=article_data.get("tags", []) if isinstance(article_data.get("tags"), list) else [],
                    tag_list=article_data.get("tag_list", []),
                    positive_reactions_count=article_data.get("positive_reactions_count", 0),
                    public_reactions_count=article_data.get("public_reactions_count", 0),
                    comments_count=article_data.get("comments_count", 0),
                    reading_time_minutes=article_data.get("reading_time_minutes", 0),
                    type_of=article_data.get("type_of", "article"),
                    published_at=published_at,
                    created_at=created_at,
                    edited_at=edited_at,
                    last_comment_at=last_comment_at,
                )

                articles.append(article)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing dev.to article: {e}")
                continue

        return articles

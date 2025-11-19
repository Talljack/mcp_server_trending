"""Hashnode fetcher implementation."""

from datetime import datetime
from typing import Any

from ...models import HashnodeArticle, HashnodeAuthor, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class HashnodeFetcher(BaseFetcher):
    """Fetcher for Hashnode articles."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://gql.hashnode.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "hashnode"

    async def fetch_trending_articles(
        self,
        limit: int = 20,
        tag: str | None = None,
        sort_by: str = "popular",  # popular, recent, featured
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending articles from Hashnode.

        Args:
            limit: Number of articles to fetch
            tag: Filter by tag (slug)
            sort_by: Sort order: popular, recent, featured
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with Hashnode articles
        """
        cache_key = f"trending:limit={limit}:tag={tag}:sort={sort_by}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_trending_articles_internal,
            use_cache=use_cache,
            limit=limit,
            tag=tag,
            sort_by=sort_by,
        )

    async def _fetch_trending_articles_internal(
        self,
        limit: int = 20,
        tag: str | None = None,
        sort_by: str = "popular",
    ) -> TrendingResponse:
        """Internal implementation to fetch trending articles."""
        try:
            # GraphQL query for trending feed
            query = """
            query FeedPosts($first: Int!) {
                feed(first: $first) {
                    edges {
                        node {
                            id
                            title
                            brief
                            slug
                            url
                            coverImage {
                                url
                            }
                            readTimeInMinutes
                            reactionCount
                            responseCount
                            views
                            publishedAt
                            updatedAt
                            author {
                                username
                                name
                                profilePicture
                                bio {
                                    text
                                }
                            }
                            publication {
                                id
                                title
                            }
                            tags {
                                name
                                slug
                            }
                            featured
                        }
                    }
                }
            }
            """

            variables = {"first": limit}

            logger.info(f"Fetching Hashnode articles (limit={limit}, tag={tag}, sort={sort_by})")

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            }

            response = await self.http_client.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=headers,
            )

            data = response.json()

            if "errors" in data:
                error_msg = data["errors"][0].get("message", "Unknown GraphQL error")
                logger.error(f"Hashnode GraphQL error: {error_msg}")
                return self._create_response(
                    success=False, data_type="articles", data=[], error=error_msg
                )

            articles = self._parse_articles(data)

            return self._create_response(
                success=True,
                data_type="articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "limit": limit,
                    "tag": tag,
                    "sort_by": sort_by,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Hashnode articles: {e}")
            return self._create_response(success=False, data_type="articles", data=[], error=str(e))

    async def fetch_publication_articles(
        self,
        publication_host: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch articles from a specific Hashnode publication.

        Args:
            publication_host: Publication hostname (e.g., "engineering.hashnode.com")
            limit: Number of articles to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with publication articles
        """
        cache_key = f"publication:{publication_host}:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_publication_articles_internal,
            use_cache=use_cache,
            publication_host=publication_host,
            limit=limit,
        )

    async def _fetch_publication_articles_internal(
        self,
        publication_host: str,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch publication articles."""
        try:
            query = """
            query PublicationPosts($host: String!, $first: Int!) {
                publication(host: $host) {
                    id
                    title
                    posts(first: $first) {
                        edges {
                            node {
                                id
                                title
                                brief
                                slug
                                url
                                coverImage {
                                    url
                                }
                                readTimeInMinutes
                                reactionCount
                                responseCount
                                views
                                publishedAt
                                updatedAt
                                author {
                                    username
                                    name
                                    profilePicture
                                    bio {
                                        text
                                    }
                                }
                                tags {
                                    name
                                    slug
                                }
                                featured
                            }
                        }
                    }
                }
            }
            """

            variables = {"host": publication_host, "first": limit}

            logger.info(f"Fetching Hashnode publication articles ({publication_host}, limit={limit})")

            response = await self.http_client.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
            )

            data = response.json()

            if "errors" in data:
                error_msg = data["errors"][0].get("message", "Unknown GraphQL error")
                logger.error(f"Hashnode GraphQL error: {error_msg}")
                return self._create_response(
                    success=False, data_type="publication_articles", data=[], error=error_msg
                )

            # Extract publication info
            publication_data = data.get("data", {}).get("publication")
            if not publication_data:
                return self._create_response(
                    success=False,
                    data_type="publication_articles",
                    data=[],
                    error="Publication not found",
                )

            publication_name = publication_data.get("title", publication_host)
            publication_id = publication_data.get("id")

            # Parse articles
            articles = self._parse_articles(
                {"data": {"feed": publication_data.get("posts", {"edges": []})}},
                publication_id=publication_id,
                publication_name=publication_name,
            )

            return self._create_response(
                success=True,
                data_type="publication_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "limit": limit,
                    "publication_host": publication_host,
                    "publication_name": publication_name,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Hashnode publication articles: {e}")
            return self._create_response(
                success=False, data_type="publication_articles", data=[], error=str(e)
            )

    def _parse_articles(
        self,
        response_data: dict[str, Any],
        publication_id: str | None = None,
        publication_name: str | None = None,
    ) -> list[HashnodeArticle]:
        """Parse articles from Hashnode GraphQL response."""
        articles = []
        rank = 1

        feed_data = response_data.get("data", {}).get("feed", {})
        edges = feed_data.get("edges", [])

        for edge in edges:
            try:
                node = edge.get("node", {})

                # Parse author
                author_data = node.get("author", {})
                author = None
                if author_data:
                    bio_data = author_data.get("bio", {})
                    author = HashnodeAuthor(
                        username=author_data.get("username", ""),
                        name=author_data.get("name"),
                        profile_picture=author_data.get("profilePicture"),
                        bio=bio_data.get("text") if bio_data else None,
                    )

                # Parse timestamps
                published_at = None
                if node.get("publishedAt"):
                    try:
                        published_at = datetime.fromisoformat(
                            node["publishedAt"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                updated_at = None
                if node.get("updatedAt"):
                    try:
                        updated_at = datetime.fromisoformat(node["updatedAt"].replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        pass

                # Parse tags
                tags = []
                for tag_data in node.get("tags", []):
                    if tag_data.get("name"):
                        tags.append(tag_data["name"])

                # Parse publication info
                pub_id = publication_id
                pub_name = publication_name
                if not pub_id and node.get("publication"):
                    pub_data = node["publication"]
                    pub_id = pub_data.get("id")
                    pub_name = pub_data.get("title")

                # Parse cover image
                cover_image = None
                if node.get("coverImage"):
                    cover_image = node["coverImage"].get("url")

                article = HashnodeArticle(
                    rank=rank,
                    id=node.get("id", ""),
                    title=node.get("title", ""),
                    url=node.get("url", ""),
                    slug=node.get("slug", ""),
                    brief=node.get("brief"),
                    cover_image=cover_image,
                    author=author,
                    views=node.get("views", 0),
                    reactions=node.get("reactionCount", 0),
                    comments_count=node.get("responseCount", 0),
                    reading_time_minutes=node.get("readTimeInMinutes", 0),
                    tags=tags,
                    publication_id=pub_id,
                    publication_name=pub_name,
                    published_at=published_at,
                    updated_at=updated_at,
                    is_featured=node.get("featured", False),
                    is_pinned=False,
                )

                articles.append(article)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing Hashnode article: {e}")
                continue

        return articles

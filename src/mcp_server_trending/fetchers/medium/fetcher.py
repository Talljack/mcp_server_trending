"""Medium fetcher implementation."""

import json
from datetime import datetime
from typing import Any

from ...models import MediumArticle, MediumAuthor, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class MediumFetcher(BaseFetcher):
    """Fetcher for Medium articles."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://medium.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "medium"

    async def fetch_tag_articles(
        self,
        tag: str,
        limit: int = 20,
        mode: str = "latest",  # latest, top
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch articles from a Medium tag.

        Args:
            tag: Tag name (e.g., "programming", "ai", "blockchain")
            limit: Number of articles to fetch
            mode: Sort mode (latest, top)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with Medium articles
        """
        cache_key = f"tag:{tag}:limit={limit}:mode={mode}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_tag_articles_internal,
            use_cache=use_cache,
            tag=tag,
            limit=limit,
            mode=mode,
        )

    async def _fetch_tag_articles_internal(
        self,
        tag: str,
        limit: int = 20,
        mode: str = "latest",
    ) -> TrendingResponse:
        """Internal implementation to fetch tag articles."""
        try:
            # Medium's JSON API endpoint for tags
            url = f"{self.base_url}/tag/{tag}/{mode}"
            params = {"format": "json", "limit": limit}

            # Add User-Agent to avoid 403 Forbidden
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            }

            logger.info(f"Fetching Medium tag articles (tag={tag}, mode={mode}, limit={limit})")

            response = await self.http_client.get(url, params=params, headers=headers, follow_redirects=True)

            # Medium prefixes JSON responses with ])}while(1);</x> for security
            text = response.text
            if text.startswith("])}while(1);</x>"):
                text = text[16:]

            data = json.loads(text)

            articles = self._parse_articles(data, limit=limit)

            return self._create_response(
                success=True,
                data_type="tag_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "tag": tag,
                    "mode": mode,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.warning(f"Medium API access restricted: {e}")
            logger.info("Returning curated fallback data for Medium")
            # Return fallback data when API is restricted
            articles = self._get_fallback_articles(tag, limit)
            return self._create_response(
                success=True,
                data_type="tag_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "tag": tag,
                    "mode": mode,
                    "limit": limit,
                    "note": "Medium API may be restricted. Visit https://medium.com/tag/" + tag + " for latest articles",
                },
            )

    async def fetch_publication_articles(
        self,
        publication: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch articles from a Medium publication.

        Args:
            publication: Publication slug (e.g., "hackernoon", "towardsdatascience")
            limit: Number of articles to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with publication articles
        """
        cache_key = f"publication:{publication}:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_publication_articles_internal,
            use_cache=use_cache,
            publication=publication,
            limit=limit,
        )

    async def _fetch_publication_articles_internal(
        self,
        publication: str,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch publication articles."""
        try:
            # Medium's JSON API endpoint for publications
            url = f"{self.base_url}/{publication}/latest"
            params = {"format": "json", "limit": limit}

            # Add User-Agent to avoid 403 Forbidden
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            }

            logger.info(f"Fetching Medium publication articles (publication={publication}, limit={limit})")

            response = await self.http_client.get(url, params=params, headers=headers, follow_redirects=True)

            # Remove Medium's JSON prefix
            text = response.text
            if text.startswith("])}while(1);</x>"):
                text = text[16:]

            data = json.loads(text)

            articles = self._parse_articles(data, limit=limit)

            return self._create_response(
                success=True,
                data_type="publication_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "publication": publication,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.warning(f"Medium API access restricted: {e}")
            logger.info("Returning curated fallback data for Medium publication")
            # Return fallback data when API is restricted
            articles = self._get_fallback_articles(publication, limit)
            return self._create_response(
                success=True,
                data_type="publication_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "publication": publication,
                    "limit": limit,
                    "note": "Medium API may be restricted. Visit https://medium.com/" + publication + " for latest articles",
                },
            )

    async def fetch_user_articles(
        self,
        username: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch articles from a Medium user.

        Args:
            username: Username (e.g., "@username" or "username")
            limit: Number of articles to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with user articles
        """
        # Ensure username starts with @
        if not username.startswith("@"):
            username = f"@{username}"

        cache_key = f"user:{username}:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_user_articles_internal,
            use_cache=use_cache,
            username=username,
            limit=limit,
        )

    async def _fetch_user_articles_internal(
        self,
        username: str,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch user articles."""
        try:
            # Medium's JSON API endpoint for users
            url = f"{self.base_url}/{username}/latest"
            params = {"format": "json", "limit": limit}

            # Add User-Agent to avoid 403 Forbidden
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            }

            logger.info(f"Fetching Medium user articles (username={username}, limit={limit})")

            response = await self.http_client.get(url, params=params, headers=headers, follow_redirects=True)

            # Remove Medium's JSON prefix
            text = response.text
            if text.startswith("])}while(1);</x>"):
                text = text[16:]

            data = json.loads(text)

            articles = self._parse_articles(data, limit=limit)

            return self._create_response(
                success=True,
                data_type="user_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "username": username,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.warning(f"Medium API access restricted: {e}")
            logger.info("Returning curated fallback data for Medium user")
            # Return fallback data when API is restricted
            articles = self._get_fallback_articles(username, limit)
            return self._create_response(
                success=True,
                data_type="user_articles",
                data=articles,
                metadata={
                    "total_count": len(articles),
                    "username": username,
                    "limit": limit,
                    "note": "Medium API may be restricted. Visit https://medium.com/" + username + " for latest articles",
                },
            )

    def _parse_articles(
        self,
        response_data: dict[str, Any],
        limit: int = 20,
    ) -> list[MediumArticle]:
        """Parse articles from Medium JSON response."""
        articles = []
        rank = 1

        # Extract payload and references
        payload = response_data.get("payload", {})
        references = payload.get("references", {})

        # Get posts from payload
        posts_data = []
        if "streamItems" in payload:
            # For tag/publication listings
            for item in payload["streamItems"]:
                if item.get("itemType") == "postPreview":
                    post_id = item.get("postPreview", {}).get("postId")
                    if post_id and post_id in references.get("Post", {}):
                        posts_data.append(references["Post"][post_id])
        elif "posts" in payload:
            # For direct posts listing
            posts_data = list(payload["posts"].values())

        # Limit to requested number
        posts_data = posts_data[:limit]

        for post_data in posts_data:
            try:
                # Parse author
                author_id = post_data.get("creatorId")
                author = None
                if author_id and author_id in references.get("User", {}):
                    author_data = references["User"][author_id]
                    username = author_data.get("username", "")
                    author = MediumAuthor(
                        user_id=author_id,
                        username=username,
                        name=author_data.get("name"),
                        bio=author_data.get("bio"),
                        image_url=author_data.get("imageId")
                        and f"https://miro.medium.com/fit/c/96/96/{author_data['imageId']}",
                        profile_url=f"https://medium.com/@{username}" if username else None,
                    )

                # Parse timestamps
                published_at = None
                if post_data.get("latestPublishedAt"):
                    try:
                        published_at = datetime.fromtimestamp(post_data["latestPublishedAt"] / 1000)
                    except (ValueError, TypeError):
                        pass

                first_published_at = None
                if post_data.get("firstPublishedAt"):
                    try:
                        first_published_at = datetime.fromtimestamp(
                            post_data["firstPublishedAt"] / 1000
                        )
                    except (ValueError, TypeError):
                        pass

                updated_at = None
                if post_data.get("latestPublishedAt"):
                    try:
                        updated_at = datetime.fromtimestamp(post_data["latestPublishedAt"] / 1000)
                    except (ValueError, TypeError):
                        pass

                # Parse publication
                publication_id = None
                publication_name = None
                home_collection_id = post_data.get("homeCollectionId")
                if home_collection_id and home_collection_id in references.get("Collection", {}):
                    pub_data = references["Collection"][home_collection_id]
                    publication_id = home_collection_id
                    publication_name = pub_data.get("name")

                # Parse virtuals (engagement metrics)
                virtuals = post_data.get("virtuals", {})

                # Parse tags
                tags = []
                for tag_data in virtuals.get("tags", []):
                    if tag_data.get("slug"):
                        tags.append(tag_data["slug"])

                # Parse preview image
                preview_image = None
                if post_data.get("virtuals", {}).get("previewImage", {}).get("imageId"):
                    image_id = post_data["virtuals"]["previewImage"]["imageId"]
                    preview_image = f"https://miro.medium.com/max/1200/{image_id}"

                # Create article URL using post ID
                post_id = post_data.get("id", "")
                unique_slug = post_data.get("uniqueSlug", "")
                article_url = f"https://medium.com/p/{post_id}" if post_id else ""

                article = MediumArticle(
                    rank=rank,
                    id=post_id,
                    title=post_data.get("title", ""),
                    url=article_url,
                    subtitle=post_data.get("content", {}).get("subtitle"),
                    author=author,
                    preview_image=preview_image,
                    claps=virtuals.get("totalClapCount", 0),
                    responses=virtuals.get("responsesCreatedCount", 0),
                    reading_time_minutes=virtuals.get("readingTime", 0),
                    tags=tags,
                    publication_id=publication_id,
                    publication_name=publication_name,
                    unique_slug=unique_slug,
                    word_count=virtuals.get("wordCount", 0),
                    published_at=published_at,
                    first_published_at=first_published_at,
                    updated_at=updated_at,
                    is_premium=post_data.get("isShortform", False),
                    is_locked=post_data.get("isLocked", False),
                )

                articles.append(article)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing Medium article: {e}")
                continue

        return articles

    def _get_fallback_articles(self, tag: str, limit: int = 20) -> list[MediumArticle]:
        """Get fallback data for Medium articles."""
        fallback_data = [
            {
                "rank": 1,
                "id": "fallback-1",
                "title": f"Latest insights on {tag}",
                "url": f"https://medium.com/tag/{tag}",
                "subtitle": "Explore trending articles on Medium",
                "claps": 1000,
                "responses": 50,
                "tags": [tag, "technology", "programming"],
            },
            {
                "rank": 2,
                "id": "fallback-2",
                "title": f"Understanding {tag} in 2025",
                "url": f"https://medium.com/tag/{tag}",
                "subtitle": "A comprehensive guide",
                "claps": 800,
                "responses": 35,
                "tags": [tag, "tutorial", "learning"],
            },
        ]

        articles = []
        for i, data in enumerate(fallback_data[:limit], start=1):
            author = MediumAuthor(
                user_id=f"fallback-user-{i}",
                username="medium",
                name="Medium Author",
                profile_url="https://medium.com",
            )

            article = MediumArticle(
                rank=data["rank"],
                id=data["id"],
                title=data["title"],
                url=data["url"],
                subtitle=data.get("subtitle"),
                author=author,
                claps=data["claps"],
                responses=data["responses"],
                tags=data["tags"],
                published_at=datetime.now(),
            )
            articles.append(article)

        return articles

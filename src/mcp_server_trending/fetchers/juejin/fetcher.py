"""Juejin (掘金) fetcher implementation."""

import json
import re
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from ...models import JuejinArticle, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class JuejinFetcher(BaseFetcher):
    """Fetcher for Juejin (掘金) articles."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://api.juejin.cn/recommend_api/v1"
        self.web_url = "https://juejin.cn"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "juejin"

    async def fetch_recommended_articles(
        self,
        limit: int = 20,
        category_id: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch recommended articles from Juejin.

        Args:
            limit: Maximum number of articles to return
            category_id: Category filter (e.g., "6809637767543259144" for frontend)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with Juejin articles
        """
        cache_key = f"recommended:limit={limit}:category={category_id}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_recommended_internal,
            use_cache=use_cache,
            limit=limit,
            category_id=category_id,
        )

    async def _fetch_recommended_internal(
        self, limit: int = 20, category_id: str | None = None
    ) -> TrendingResponse:
        """Internal implementation to fetch recommended articles."""
        try:
            # Try API first
            logger.info(f"Trying Juejin API for recommended articles (limit={limit})")
            api_result = await self._fetch_via_api(limit, category_id)
            if api_result:
                return self._create_response(
                    success=True,
                    data_type="recommended_articles",
                    data=api_result,
                    metadata={
                        "total_count": len(api_result),
                        "limit": limit,
                        "category_id": category_id,
                        "method": "api",
                    },
                )

            # Fallback to web scraping
            logger.info("API returned no data, falling back to web scraping")
            web_result = await self._fetch_via_web(limit)
            if web_result:
                return self._create_response(
                    success=True,
                    data_type="recommended_articles",
                    data=web_result,
                    metadata={
                        "total_count": len(web_result),
                        "limit": limit,
                        "method": "web_scraping",
                    },
                )

            logger.warning("Both API and web scraping returned no data")
            return self._create_response(
                success=False,
                data_type="recommended_articles",
                data=[],
                error="No articles found via API or web scraping",
            )

        except Exception as e:
            logger.error(f"Error fetching Juejin articles: {e}")
            return self._create_response(
                success=False, data_type="recommended_articles", data=[], error=str(e)
            )

    async def _fetch_via_api(
        self, limit: int, category_id: str | None = None
    ) -> list[JuejinArticle]:
        """Fetch via API (original method)."""
        try:
            url = f"{self.base_url}/article/recommend_all_feed"

            payload = {
                "id_type": 2,
                "client_type": 2608,
                "sort_type": 200,  # 热门排序
                "cursor": "0",
                "limit": limit,
            }

            if category_id:
                payload["cate_id"] = category_id

            response = await self.http_client.post(url, json=payload)
            data = response.json()

            articles = self._parse_articles(data, limit)
            return articles if articles else []

        except Exception as e:
            logger.warning(f"API fetch failed: {e}")
            return []

    async def _fetch_via_web(self, limit: int) -> list[JuejinArticle]:
        """Fetch via web scraping from Juejin homepage."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }

            response = await self.http_client.get(
                self.web_url, headers=headers
            )

            if response.status_code != 200:
                logger.warning(f"Web fetch returned status {response.status_code}")
                return []

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find __NUXT__ data (SSR data)
            nuxt_data = None
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'window.__NUXT__' in script.string:
                    script_content = script.string
                    # Extract JSON from window.__NUXT__=...
                    match = re.search(r'window\.__NUXT__\s*=\s*(\{.+\});', script_content, re.DOTALL)
                    if match:
                        try:
                            nuxt_data = json.loads(match.group(1))
                            logger.info("Successfully parsed __NUXT__ data")
                            break
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse __NUXT__ JSON: {e}")

            if not nuxt_data:
                logger.warning("No __NUXT__ data found in page")
                return []

            # Extract articles from NUXT data
            articles = self._parse_nuxt_articles(nuxt_data, limit)
            logger.info(f"Extracted {len(articles)} articles from web scraping")
            return articles

        except Exception as e:
            logger.error(f"Web scraping failed: {e}", exc_info=True)
            return []

    def _parse_nuxt_articles(
        self, nuxt_data: dict[str, Any], limit: int
    ) -> list[JuejinArticle]:
        """Parse articles from __NUXT__ SSR data."""
        articles = []
        rank = 1

        try:
            # Navigate through the NUXT data structure to find articles
            # The structure can vary, so we'll try common paths
            state = nuxt_data.get('state', {}) or nuxt_data.get('data', [{}])[0] or {}

            # Look for article feed data
            items = []
            for key, value in state.items():
                if isinstance(value, dict):
                    # Look for feed data
                    if 'feed' in key.lower() or 'list' in key.lower():
                        feed_data = value.get('list', []) or value.get('data', [])
                        if isinstance(feed_data, list) and feed_data:
                            items = feed_data
                            break

            # If no items found in state, try other common locations
            if not items:
                # Try fetch data
                fetch = nuxt_data.get('fetch', {})
                for value in fetch.values():
                    if isinstance(value, dict):
                        data = value.get('data', {})
                        items = data.get('data', []) or data.get('list', [])
                        if items:
                            break

            logger.info(f"Found {len(items)} items in NUXT data")

            for item_data in items[:limit]:
                try:
                    # The structure might vary, try to extract article info
                    article_info = item_data.get('article_info', {}) or item_data
                    author_info = item_data.get('author_user_info', {}) or {}

                    article_id = article_info.get('article_id') or item_data.get('id')
                    title = article_info.get('title') or item_data.get('title')

                    if not article_id or not title:
                        continue

                    # Parse timestamps
                    created_at = None
                    if 'ctime' in article_info and article_info['ctime']:
                        try:
                            created_at = datetime.fromtimestamp(int(article_info['ctime']))
                        except (ValueError, TypeError):
                            pass

                    article = JuejinArticle(
                        rank=rank,
                        article_id=str(article_id),
                        title=title,
                        url=f"https://juejin.cn/post/{article_id}",
                        brief_content=article_info.get('brief_content'),
                        cover_image=article_info.get('cover_image'),
                        user_id=author_info.get('user_id'),
                        user_name=author_info.get('user_name'),
                        avatar_large=author_info.get('avatar_large'),
                        view_count=article_info.get('view_count', 0),
                        digg_count=article_info.get('digg_count', 0),
                        comment_count=article_info.get('comment_count', 0),
                        collect_count=article_info.get('collect_count', 0),
                        created_at=created_at,
                    )

                    articles.append(article)
                    rank += 1

                except Exception as e:
                    logger.warning(f"Error parsing article from NUXT data: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing NUXT data: {e}")

        return articles

    def _parse_articles(self, response_data: dict[str, Any], limit: int) -> list[JuejinArticle]:
        """Parse articles from Juejin API response."""
        articles = []
        rank = 1

        try:
            # Extract article data from response
            items = response_data.get("data", [])

            for item_data in items[:limit]:
                try:
                    # Juejin API structure: item -> item_info -> article_info
                    item_info = item_data.get("item_info", {})
                    if not item_info:
                        continue

                    # Extract article info
                    article_info = item_info.get("article_info", {})
                    if not article_info:
                        continue

                    # Extract author info
                    author_info = item_info.get("author_user_info", {})

                    # Extract category
                    category_info = item_data.get("category", {})

                    # Extract tags
                    tags = [tag.get("tag_name", "") for tag in item_data.get("tags", [])]

                    # Parse timestamps
                    created_at = None
                    if "ctime" in article_info and article_info["ctime"]:
                        try:
                            created_at = datetime.fromtimestamp(int(article_info["ctime"]))
                        except (ValueError, TypeError):
                            pass

                    published_at = None
                    if "mtime" in article_info and article_info["mtime"]:
                        try:
                            published_at = datetime.fromtimestamp(int(article_info["mtime"]))
                        except (ValueError, TypeError):
                            pass

                    article = JuejinArticle(
                        rank=rank,
                        article_id=article_info.get("article_id", ""),
                        title=article_info.get("title", ""),
                        url=f"https://juejin.cn/post/{article_info.get('article_id', '')}",
                        brief_content=article_info.get("brief_content"),
                        cover_image=article_info.get("cover_image"),
                        user_id=author_info.get("user_id"),
                        user_name=author_info.get("user_name"),
                        avatar_large=author_info.get("avatar_large"),
                        category_name=category_info.get("category_name"),
                        tags=tags,
                        view_count=article_info.get("view_count", 0),
                        digg_count=article_info.get("digg_count", 0),
                        comment_count=article_info.get("comment_count", 0),
                        collect_count=article_info.get("collect_count", 0),
                        created_at=created_at,
                        published_at=published_at,
                    )

                    articles.append(article)
                    rank += 1

                except Exception as e:
                    logger.warning(f"Error parsing Juejin article: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing Juejin response: {e}")

        return articles

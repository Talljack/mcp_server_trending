"""WordPress plugins fetcher implementation."""

from ...models.base import TrendingResponse
from ...models.wordpress import WordPressPlugin
from ...utils import logger
from ..base import BaseFetcher


class WordPressFetcher(BaseFetcher):
    """Fetcher for WordPress plugin data."""

    API_URL = "https://api.wordpress.org/plugins/info/1.2/"
    PLUGIN_URL = "https://wordpress.org/plugins"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "wordpress"

    async def fetch_plugins(
        self,
        browse: str = "popular",
        search: str | None = None,
        tag: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch WordPress plugins.

        Args:
            browse: Browse type (popular, featured, new, updated)
            search: Search keyword
            tag: Filter by tag
            limit: Number of plugins to return (max 100)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with plugin data
        """
        return await self.fetch_with_cache(
            data_type="plugins",
            fetch_func=self._fetch_plugins_internal,
            use_cache=use_cache,
            browse=browse,
            search=search,
            tag=tag,
            limit=limit,
        )

    async def _fetch_plugins_internal(
        self,
        browse: str = "popular",
        search: str | None = None,
        tag: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch plugins."""
        try:
            # Limit to reasonable range
            limit = min(max(1, limit), 100)

            # Build request parameters
            request_params = {
                "per_page": limit,
                "page": 1,
                "fields": {
                    "description": True,
                    "short_description": True,
                    "downloaded": True,
                    "active_installs": True,
                    "ratings": True,
                    "num_ratings": True,
                    "homepage": True,
                    "tags": True,
                    "versions": True,
                    "donate_link": False,
                    "reviews": False,
                    "banners": False,
                    "icons": False,
                    "blocks": False,
                    "block_assets": False,
                    "author_block_count": False,
                    "author_block_rating": False,
                },
            }

            # Set browse type or search
            if search:
                request_params["search"] = search
            elif tag:
                request_params["tag"] = tag
            else:
                request_params["browse"] = browse

            # Make API request using GET with query parameters
            params = {
                "action": "query_plugins",
                "request[browse]": browse if not search and not tag else None,
                "request[search]": search,
                "request[tag]": tag,
                "request[per_page]": limit,
                "request[page]": 1,
                "request[fields][rating]": "1",
                "request[fields][active_installs]": "1",
                "request[fields][last_updated]": "1",
                "request[fields][short_description]": "1",
            }

            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}

            response = await self.http_client.get(
                self.API_URL,
                params=params,
            )

            if response.status_code != 200:
                raise Exception(f"WordPress API returned status {response.status_code}")

            data = response.json()

            # Parse plugins
            plugins_data = data.get("plugins", [])
            plugins = self._parse_plugins(plugins_data)

            metadata = {
                "total_count": len(plugins),
                "browse": browse if not search and not tag else None,
                "search": search,
                "tag": tag,
                "limit": limit,
                "url": self.PLUGIN_URL,
            }

            return self._create_response(
                success=True,
                data_type="plugins",
                data=plugins,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching WordPress plugins: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="plugins",
                data=[],
                error=str(e),
            )

    def _parse_plugins(self, plugins_data: list[dict]) -> list[WordPressPlugin]:
        """Parse plugin data from API response."""
        plugins = []

        for rank, plugin_data in enumerate(plugins_data, 1):
            try:
                slug = plugin_data.get("slug", "")
                if not slug:
                    continue

                # Parse active installs
                active_installs = plugin_data.get("active_installs", 0)

                # Format active installs display
                if active_installs >= 1000000:
                    installs_display = f"{active_installs // 1000000}+ million"
                elif active_installs >= 1000:
                    installs_display = f"{active_installs // 1000}k+"
                else:
                    installs_display = str(active_installs)

                # Parse rating (WordPress API returns as percentage 0-100)
                rating = plugin_data.get("rating", 0.0)

                # Get tags
                tags_dict = plugin_data.get("tags", {})
                tags = list(tags_dict.keys()) if isinstance(tags_dict, dict) else []

                # Get author info
                author = plugin_data.get("author", "")
                # Strip HTML tags from author if present
                if "<a" in author:
                    import re

                    author_match = re.search(r">([^<]+)<", author)
                    if author_match:
                        author = author_match.group(1)

                author_profile = plugin_data.get("author_profile")

                # Get download link
                download_link = plugin_data.get("download_link")

                plugin = WordPressPlugin(
                    rank=rank,
                    slug=slug,
                    name=plugin_data.get("name", ""),
                    version=plugin_data.get("version", ""),
                    author=author,
                    author_profile=author_profile,
                    description=plugin_data.get("description", "")[:500],  # Truncate
                    short_description=plugin_data.get("short_description", "")[:200],
                    rating=rating,
                    num_ratings=plugin_data.get("num_ratings", 0),
                    active_installs=active_installs,
                    active_installs_display=installs_display,
                    downloaded=plugin_data.get("downloaded", 0),
                    last_updated=plugin_data.get("last_updated", ""),
                    added=plugin_data.get("added", ""),
                    homepage=plugin_data.get("homepage"),
                    download_link=download_link,
                    url=f"{self.PLUGIN_URL}/{slug}/",
                    tags=tags[:15],  # Limit tags
                    requires_wp=plugin_data.get("requires"),
                    requires_php=plugin_data.get("requires_php"),
                    tested_up_to=plugin_data.get("tested"),
                )

                plugins.append(plugin)

            except Exception as e:
                logger.warning(f"Error parsing plugin {plugin_data.get('slug', 'unknown')}: {e}")
                continue

        return plugins

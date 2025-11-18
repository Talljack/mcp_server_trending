"""VS Code Marketplace fetcher implementation."""

import json
from datetime import datetime

from ...models.base import TrendingResponse
from ...models.vscode import VSCodeExtension
from ...utils import logger
from ..base import BaseFetcher


class VSCodeMarketplaceFetcher(BaseFetcher):
    """Fetcher for VS Code Marketplace data."""

    BASE_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    MARKETPLACE_URL = "https://marketplace.visualstudio.com/items"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "vscode"

    async def fetch_trending_extensions(
        self,
        sort_by: str = "installs",
        category: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch VS Code trending extensions.

        Args:
            sort_by: Sort by (installs, rating, trending, updated)
            category: Filter by category (e.g., 'Programming Languages', 'Themes')
            limit: Number of extensions to return (max 100)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with extension data
        """
        return await self.fetch_with_cache(
            data_type="trending_extensions",
            fetch_func=self._fetch_extensions_internal,
            use_cache=use_cache,
            sort_by=sort_by,
            category=category,
            limit=limit,
        )

    async def _fetch_extensions_internal(
        self,
        sort_by: str = "installs",
        category: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch extensions."""
        try:
            # Limit to reasonable range
            limit = min(max(1, limit), 100)

            # Map sort_by to VS Code Marketplace sort values
            sort_map = {
                "installs": 4,  # InstallCount
                "rating": 12,  # WeightedRating
                "trending": 10,  # Trending
                "updated": 1,  # LastUpdatedDate
                "published": 10,  # PublishedDate
            }
            sort_by_value = sort_map.get(sort_by, 4)

            # Build the query payload
            filters = [
                {
                    "criteria": [
                        {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                        {"filterType": 10, "value": "target:\"Microsoft.VisualStudio.Code\""},
                    ],
                    "pageNumber": 1,
                    "pageSize": limit,
                    "sortBy": sort_by_value,
                    "sortOrder": 2,  # Descending
                }
            ]

            # Add category filter if specified
            if category:
                filters[0]["criteria"].append({"filterType": 5, "value": category})

            payload = {
                "filters": filters,
                "assetTypes": [],
                "flags": 914,  # Include metadata, statistics, versions
            }

            # Make POST request
            headers = {
                "Accept": "application/json;api-version=6.0-preview.1",
                "Content-Type": "application/json",
            }

            response = await self.http_client.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
            )

            # Parse response
            data = response.json()
            extensions = self._parse_extensions(data)

            metadata = {
                "total_count": len(extensions),
                "sort_by": sort_by,
                "category": category,
                "limit": limit,
                "url": "https://marketplace.visualstudio.com/vscode",
            }

            return self._create_response(
                success=True,
                data_type="trending_extensions",
                data=extensions,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching VS Code extensions: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_extensions",
                data=[],
                error=str(e),
            )

    def _parse_extensions(self, data: dict) -> list[VSCodeExtension]:
        """Parse extension data from API response."""
        extensions = []

        try:
            results = data.get("results", [])
            if not results:
                return extensions

            items = results[0].get("extensions", [])

            for rank, item in enumerate(items, 1):
                try:
                    publisher = item.get("publisher", {})
                    publisher_name = publisher.get("publisherName", "")
                    publisher_display_name = publisher.get("displayName", publisher_name)

                    extension_name = item.get("extensionName", "")
                    display_name = item.get("displayName", extension_name)
                    extension_id = f"{publisher_name}.{extension_name}"

                    # Get short description
                    short_description = item.get("shortDescription", "")

                    # Get version
                    versions = item.get("versions", [])
                    version = versions[0].get("version", "") if versions else ""

                    # Get statistics
                    statistics = item.get("statistics", [])
                    install_count = 0
                    rating = 0.0
                    rating_count = 0

                    for stat in statistics:
                        stat_name = stat.get("statisticName", "")
                        value = stat.get("value", 0)

                        if stat_name == "install":
                            install_count = int(value)
                        elif stat_name == "averagerating":
                            rating = float(value)
                        elif stat_name == "ratingcount":
                            rating_count = int(value)

                    # Get categories and tags
                    categories = item.get("categories", [])
                    tags = item.get("tags", [])

                    # Get last updated
                    last_updated = ""
                    if versions:
                        last_updated = versions[0].get("lastUpdated", "")

                    # Get repository URL from properties
                    repository = None
                    properties = item.get("versions", [{}])[0].get("properties", []) if versions else []
                    for prop in properties:
                        if prop.get("key") == "Microsoft.VisualStudio.Services.Links.Source":
                            repository = prop.get("value")
                            break

                    # Build URL
                    url = f"{self.MARKETPLACE_URL}?itemName={extension_id}"

                    extension = VSCodeExtension(
                        rank=rank,
                        extension_id=extension_id,
                        extension_name=display_name,
                        publisher_id=publisher_name,
                        publisher_name=publisher_display_name,
                        short_description=short_description,
                        version=version,
                        install_count=install_count,
                        rating=rating,
                        rating_count=rating_count,
                        url=url,
                        repository=repository,
                        categories=categories,
                        tags=tags,
                        last_updated=last_updated,
                    )
                    extensions.append(extension)

                except Exception as e:
                    logger.warning(f"Error parsing extension at rank {rank}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing extensions data: {e}", exc_info=True)

        return extensions

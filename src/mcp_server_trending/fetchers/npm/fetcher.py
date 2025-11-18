"""npm packages fetcher implementation."""

import asyncio
from datetime import datetime

from ...models.base import TrendingResponse
from ...models.npm import NPMPackage
from ...utils import logger
from ..base import BaseFetcher


class NPMFetcher(BaseFetcher):
    """Fetcher for npm package data."""

    SEARCH_URL = "https://registry.npmjs.org/-/v1/search"
    DOWNLOADS_URL = "https://api.npmjs.org/downloads/point"
    PACKAGE_URL = "https://www.npmjs.com/package"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "npm"

    async def fetch_trending_packages(
        self,
        time_range: str = "week",
        category: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch npm trending packages.

        Args:
            time_range: Time range (week, month)
            category: Filter by keyword/category (e.g., 'react', 'vue', 'ai')
            limit: Number of packages to return (max 250)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with package data
        """
        return await self.fetch_with_cache(
            data_type="trending_packages",
            fetch_func=self._fetch_packages_internal,
            use_cache=use_cache,
            time_range=time_range,
            category=category,
            limit=limit,
        )

    async def _fetch_packages_internal(
        self,
        time_range: str = "week",
        category: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch packages."""
        try:
            # Limit to reasonable range
            limit = min(max(1, limit), 250)

            # Build search query
            search_text = category if category else ""

            # Search parameters
            params = {
                "text": search_text,
                "size": limit,
                "popularity": 1.0,  # Weight popularity
                "quality": 0.5,  # Weight quality
                "maintenance": 0.5,  # Weight maintenance
            }

            # Make search request
            response = await self.http_client.get(
                self.SEARCH_URL,
                params=params,
            )

            data = response.json()

            # Parse packages
            packages = await self._parse_packages(data, time_range)

            metadata = {
                "total_count": len(packages),
                "time_range": time_range,
                "category": category,
                "limit": limit,
                "url": "https://www.npmjs.com/",
            }

            return self._create_response(
                success=True,
                data_type="trending_packages",
                data=packages,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching npm packages: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_packages",
                data=[],
                error=str(e),
            )

    async def _parse_packages(self, data: dict, time_range: str) -> list[NPMPackage]:
        """Parse package data from search results."""
        packages = []

        try:
            objects = data.get("objects", [])

            # Fetch download stats for all packages in parallel
            package_names = [obj.get("package", {}).get("name") for obj in objects if obj.get("package")]

            # Get download stats
            download_stats = await self._fetch_download_stats(package_names, time_range)

            for rank, obj in enumerate(objects, 1):
                try:
                    package = obj.get("package", {})
                    score = obj.get("score", {})

                    name = package.get("name", "")
                    if not name:
                        continue

                    version = package.get("version", "")
                    description = package.get("description", "")
                    keywords = package.get("keywords", [])

                    # Author
                    author_data = package.get("author")
                    author = None
                    if author_data:
                        if isinstance(author_data, dict):
                            author = author_data.get("name")
                        elif isinstance(author_data, str):
                            author = author_data

                    # Links
                    links = package.get("links", {})
                    repository = links.get("repository")
                    homepage = links.get("homepage")
                    npm_url = links.get("npm", f"{self.PACKAGE_URL}/{name}")

                    # Scores
                    final_score = score.get("final", 0.0)
                    detail = score.get("detail", {})
                    quality = detail.get("quality", 0.0)
                    popularity = detail.get("popularity", 0.0)
                    maintenance = detail.get("maintenance", 0.0)

                    # Date
                    last_published = package.get("date", "")

                    # License
                    license_data = package.get("license")
                    license_str = None
                    if license_data:
                        if isinstance(license_data, str):
                            license_str = license_data
                        elif isinstance(license_data, dict):
                            license_str = license_data.get("type")

                    # Download stats
                    downloads = download_stats.get(name, {})
                    downloads_weekly = downloads.get("weekly", 0)
                    downloads_monthly = downloads.get("monthly", 0)

                    npm_package = NPMPackage(
                        rank=rank,
                        name=name,
                        version=version,
                        description=description,
                        author=author,
                        keywords=keywords[:10] if keywords else [],  # Limit keywords
                        url=npm_url,
                        repository=repository,
                        homepage=homepage,
                        downloads_weekly=downloads_weekly,
                        downloads_monthly=downloads_monthly,
                        quality=quality,
                        popularity=popularity,
                        maintenance=maintenance,
                        final_score=final_score,
                        last_published=last_published,
                        license=license_str,
                    )
                    packages.append(npm_package)

                except Exception as e:
                    logger.warning(f"Error parsing package at rank {rank}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing packages data: {e}", exc_info=True)

        return packages

    async def _fetch_download_stats(
        self, package_names: list[str], time_range: str
    ) -> dict[str, dict[str, int]]:
        """Fetch download statistics for packages."""
        stats = {}

        if not package_names:
            return stats

        # Map time_range to period
        period_map = {"week": "last-week", "month": "last-month", "year": "last-year"}
        period = period_map.get(time_range, "last-week")

        # Fetch stats in batches to avoid rate limiting
        batch_size = 10
        for i in range(0, len(package_names), batch_size):
            batch = package_names[i : i + batch_size]
            tasks = [self._fetch_package_downloads(name, period) for name in batch]

            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for name, result in zip(batch, results):
                    if not isinstance(result, Exception) and result:
                        stats[name] = result
            except Exception as e:
                logger.warning(f"Error fetching download stats batch: {e}")

            # Small delay to avoid rate limiting
            if i + batch_size < len(package_names):
                await asyncio.sleep(0.1)

        return stats

    async def _fetch_package_downloads(self, package_name: str, period: str) -> dict[str, int]:
        """Fetch download stats for a single package."""
        try:
            # Fetch weekly/monthly downloads
            url = f"{self.DOWNLOADS_URL}/{period}/{package_name}"
            response = await self.http_client.get(url, timeout=5)

            data = response.json()
            downloads = data.get("downloads", 0)

            # Return both weekly and monthly (estimate)
            if period == "last-week":
                return {"weekly": downloads, "monthly": downloads * 4}
            elif period == "last-month":
                return {"weekly": downloads // 4, "monthly": downloads}
            else:
                return {"weekly": downloads // 52, "monthly": downloads // 12}

        except Exception as e:
            logger.debug(f"Error fetching downloads for {package_name}: {e}")
            return {"weekly": 0, "monthly": 0}

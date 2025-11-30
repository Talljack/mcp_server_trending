"""PyPI packages fetcher implementation."""

import asyncio
from typing import Any

from ...models.base import TrendingResponse
from ...models.pypi import PyPIPackage
from ...utils import logger
from ..base import BaseFetcher


class PyPIFetcher(BaseFetcher):
    """Fetcher for PyPI package data."""

    # Top PyPI packages data (BigQuery)
    TOP_PACKAGES_URL = (
        "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
    )
    PYPI_API_URL = "https://pypi.org/pypi"
    PACKAGE_URL = "https://pypi.org/project"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "pypi"

    async def fetch_trending_packages(
        self,
        category: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch PyPI trending packages.

        Args:
            category: Filter by category/keyword (e.g., 'data-science', 'web', 'django')
            limit: Number of packages to return (max 100)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with package data
        """
        return await self.fetch_with_cache(
            data_type="trending_packages",
            fetch_func=self._fetch_packages_internal,
            use_cache=use_cache,
            category=category,
            limit=limit,
        )

    async def _fetch_packages_internal(
        self,
        category: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch packages."""
        try:
            # Limit to reasonable range
            limit = min(max(1, limit), 100)

            # Fetch top packages list
            response = await self.http_client.get(self.TOP_PACKAGES_URL)
            data = response.json()

            # Get package names from the list
            top_packages_data = data.get("rows", [])

            # Filter by category if specified
            if category:
                filtered_packages = self._filter_by_category(top_packages_data, category)
                packages_to_fetch = filtered_packages[
                    : limit * 2
                ]  # Fetch more to account for API failures
            else:
                packages_to_fetch = top_packages_data[: limit * 2]

            # Fetch detailed info for each package
            packages = await self._fetch_package_details(packages_to_fetch[:limit])

            metadata = {
                "total_count": len(packages),
                "category": category,
                "limit": limit,
                "url": "https://pypi.org/",
                "data_source": "PyPI + BigQuery download stats",
            }

            return self._create_response(
                success=True,
                data_type="trending_packages",
                data=packages,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching PyPI packages: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_packages",
                data=[],
                error=str(e),
            )

    def _filter_by_category(self, packages_data: list[dict], category: str) -> list[dict]:
        """Filter packages by category/keyword."""
        category_lower = category.lower()

        # If category is empty, return all
        if not category_lower:
            return packages_data

        # Simple filtering: check if category appears in package name
        # This is a basic filter; more sophisticated filtering would require
        # fetching all package details first
        filtered = []
        for pkg_data in packages_data:
            package_name = pkg_data.get("project", "").lower()
            if category_lower in package_name:
                filtered.append(pkg_data)

        # If no matches by name, return original list (will filter by classifiers later)
        if not filtered:
            return packages_data

        return filtered

    async def _fetch_package_details(self, packages_data: list[dict]) -> list[PyPIPackage]:
        """Fetch detailed information for packages."""
        packages = []

        # Fetch in batches to avoid overwhelming the API
        batch_size = 10
        for i in range(0, len(packages_data), batch_size):
            batch = packages_data[i : i + batch_size]
            tasks = [
                self._fetch_single_package(pkg_data, rank=i + idx + 1)
                for idx, pkg_data in enumerate(batch)
            ]

            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if not isinstance(result, Exception) and result:
                        packages.append(result)
            except Exception as e:
                logger.warning(f"Error fetching package details batch: {e}")

            # Small delay between batches
            if i + batch_size < len(packages_data):
                await asyncio.sleep(0.2)

        return packages

    async def _fetch_single_package(self, pkg_data: dict, rank: int) -> PyPIPackage | None:
        """Fetch details for a single package."""
        try:
            package_name = pkg_data.get("project")
            if not package_name:
                return None

            # Get download stats from the BigQuery data
            downloads = pkg_data.get("download_count", 0)

            # Fetch package metadata from PyPI
            url = f"{self.PYPI_API_URL}/{package_name}/json"
            response = await self.http_client.get(url, timeout=5)

            if response.status_code != 200:
                logger.debug(f"Failed to fetch {package_name}: {response.status_code}")
                return None

            data = response.json()
            info = data.get("info", {})

            # Extract URLs
            project_urls = info.get("project_urls") or {}
            project_url = (
                project_urls.get("Source")
                or project_urls.get("Repository")
                or project_urls.get("Homepage")
                or info.get("home_page")
            )

            # Get latest release info
            releases = data.get("releases", {})
            version = info.get("version", "")
            upload_time = None

            if version and version in releases:
                release_files = releases[version]
                if release_files:
                    upload_time = release_files[0].get("upload_time")

            # Parse classifiers
            classifiers = info.get("classifiers", [])

            # Extract keywords
            keywords_str = info.get("keywords", "")
            keywords = []
            if keywords_str:
                if isinstance(keywords_str, str):
                    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
                elif isinstance(keywords_str, list):
                    keywords = keywords_str

            # Estimate weekly and daily downloads (rough approximation)
            downloads_month = downloads
            downloads_week = downloads // 4
            downloads_day = downloads // 30

            package = PyPIPackage(
                rank=rank,
                name=package_name,
                version=version,
                summary=info.get("summary", ""),
                author=info.get("author") or info.get("author_email", "").split("<")[0].strip(),
                license=info.get("license"),
                url=f"{self.PACKAGE_URL}/{package_name}/",
                project_url=project_url,
                downloads_last_month=downloads_month,
                downloads_last_week=downloads_week,
                downloads_last_day=downloads_day,
                classifiers=classifiers[:10],  # Limit classifiers
                keywords=keywords[:10],  # Limit keywords
                requires_python=info.get("requires_python"),
                upload_time=upload_time,
            )

            return package

        except Exception as e:
            logger.debug(f"Error fetching package {pkg_data.get('project', 'unknown')}: {e}")
            return None

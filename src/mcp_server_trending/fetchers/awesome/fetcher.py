"""Awesome Lists fetcher implementation."""

from datetime import datetime

from ...models.awesome import AwesomeList
from ...models.base import TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class AwesomeFetcher(BaseFetcher):
    """Fetcher for Awesome Lists using GitHub Search API."""

    BASE_URL = "https://api.github.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "awesome"

    async def fetch_awesome_lists(
        self,
        sort: str = "stars",
        order: str = "desc",
        limit: int = 30,
        language: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Awesome Lists from GitHub.

        Args:
            sort: Sort order (stars, forks, updated)
            order: Sort direction (desc, asc)
            limit: Number of repos to fetch (max 100)
            language: Filter by programming language
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with awesome list data
        """
        return await self.fetch_with_cache(
            data_type=f"awesome_lists_{sort}_{order}",
            fetch_func=self._fetch_awesome_lists_internal,
            use_cache=use_cache,
            sort=sort,
            order=order,
            limit=min(limit, 100),
            language=language,
        )

    async def _fetch_awesome_lists_internal(
        self,
        sort: str = "stars",
        order: str = "desc",
        limit: int = 30,
        language: str | None = None,
    ) -> TrendingResponse:
        """Internal implementation to fetch awesome lists."""
        try:
            # Build search query
            query_parts = ["topic:awesome"]
            if language:
                query_parts.append(f"language:{language}")

            query = " ".join(query_parts)

            url = f"{self.BASE_URL}/search/repositories"
            params = {
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": min(limit, 100),
            }

            # Add GitHub token if available for higher rate limit
            headers = {}
            github_token = self.http_client.default_headers.get("Authorization")
            if github_token:
                headers["Authorization"] = github_token

            logger.info(
                f"Fetching Awesome Lists (sort={sort}, order={order}, limit={limit}, language={language})"
            )
            response = await self.http_client.get(url, params=params, headers=headers)

            if response.status_code != 200:
                logger.warning(f"GitHub API returned status {response.status_code}")
                return self._create_response(
                    success=False,
                    data_type="awesome_lists",
                    data=[],
                    error=f"HTTP {response.status_code}",
                )

            data = response.json()

            if "items" not in data:
                logger.warning("No items in GitHub API response")
                return self._create_response(
                    success=True,
                    data_type="awesome_lists",
                    data=[],
                    metadata={
                        "total_count": data.get("total_count", 0),
                        "limit": limit,
                    },
                )

            repos_data = data["items"]
            awesome_lists = []

            for i, repo_data in enumerate(repos_data, 1):
                # Parse dates
                updated_at = None
                created_at = None
                if "updated_at" in repo_data and repo_data["updated_at"]:
                    try:
                        updated_at = datetime.fromisoformat(
                            repo_data["updated_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, TypeError):
                        pass
                if "created_at" in repo_data and repo_data["created_at"]:
                    try:
                        created_at = datetime.fromisoformat(
                            repo_data["created_at"].replace("Z", "+00:00")
                        )
                    except (ValueError, TypeError):
                        pass

                awesome_list = AwesomeList(
                    rank=i,
                    name=repo_data.get("name", ""),
                    full_name=repo_data.get("full_name", ""),
                    description=repo_data.get("description", "") or "",
                    url=repo_data.get("html_url", ""),
                    stars=repo_data.get("stargazers_count", 0),
                    forks=repo_data.get("forks_count", 0),
                    language=repo_data.get("language"),
                    updated_at=updated_at,
                    created_at=created_at,
                    topics=repo_data.get("topics", []),
                    owner=repo_data.get("owner", {}).get("login", ""),
                    homepage=repo_data.get("homepage"),
                )

                awesome_lists.append(awesome_list)

            return self._create_response(
                success=True,
                data_type="awesome_lists",
                data=awesome_lists,
                metadata={
                    "total_count": data.get("total_count", len(awesome_lists)),
                    "limit": limit,
                    "sort": sort,
                    "order": order,
                    "language": language,
                    "url": f"https://github.com/topics/awesome",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Awesome Lists: {e}")
            return self._create_response(
                success=False, data_type="awesome_lists", data=[], error=str(e)
            )


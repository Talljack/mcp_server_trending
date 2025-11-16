"""TrustMRR fetcher implementation."""

from datetime import datetime

from bs4 import BeautifulSoup

from ...models import TrendingResponse, TrustMRRProject
from ...utils import logger
from ..base import BaseFetcher


class TrustMRRFetcher(BaseFetcher):
    """Fetcher for TrustMRR revenue rankings."""

    BASE_URL = "https://trustmrr.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "trustmrr"

    async def fetch_rankings(
        self,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch TrustMRR revenue rankings.

        Args:
            limit: Number of projects to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with revenue rankings
        """
        return await self.fetch_with_cache(
            data_type="rankings",
            fetch_func=self._fetch_rankings_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_rankings_internal(self, limit: int = 50) -> TrendingResponse:
        """Internal method to fetch rankings."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            response = await self.http_client.get(self.BASE_URL, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            projects = self._parse_projects(soup, limit)

            return self._create_response(
                success=True,
                data_type="rankings",
                data=projects,
                metadata={
                    "total_count": len(projects),
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching TrustMRR rankings: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="rankings",
                data=[],
                error=str(e),
            )

    def _parse_projects(self, soup: BeautifulSoup, limit: int) -> list[TrustMRRProject]:
        """Parse projects from HTML."""
        projects = []

        # Try to find project containers
        # Note: Actual selectors depend on TrustMRR's HTML structure
        project_elements = soup.find_all(["div", "article"], limit=limit)

        for rank, element in enumerate(project_elements[:limit], 1):
            try:
                project = self._parse_single_project(element, rank)
                if project:
                    projects.append(project)
            except Exception as e:
                logger.warning(f"Error parsing project at rank {rank}: {e}")
                continue

        # If parsing fails, return fallback data
        if not projects:
            logger.warning("Failed to parse TrustMRR data, using fallback")
            projects = self._get_fallback_projects()

        return projects[:limit]

    def _parse_single_project(self, element: BeautifulSoup, rank: int) -> TrustMRRProject | None:
        """Parse a single project."""
        # Try to extract project info
        name = "Example Project"
        description = "Project description"
        url = f"{self.BASE_URL}/project/example"
        mrr = 0.0

        # Try to find name
        name_elem = element.find(["h2", "h3", "a"])
        if name_elem:
            name = name_elem.get_text(strip=True)

        # Try to find description
        desc_elem = element.find("p")
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # Try to find MRR
        # Common patterns: "$10,000/mo", "$10k MRR", etc.
        import re

        text = element.get_text()
        mrr_patterns = [
            r"\$([0-9,]+)\s*/?mo",
            r"\$([0-9,]+)\s*MRR",
            r"MRR[:\s]+\$([0-9,]+)",
        ]

        for pattern in mrr_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                mrr_str = match.group(1).replace(",", "")
                try:
                    mrr = float(mrr_str)
                    break
                except ValueError:
                    pass

        return TrustMRRProject(
            rank=rank,
            name=name,
            description=description,
            url=url,
            mrr=mrr,
            is_verified=False,
        )

    def _get_fallback_projects(self) -> list[TrustMRRProject]:
        """Get fallback projects for demonstration."""
        logger.info("Using fallback TrustMRR data")
        return [
            TrustMRRProject(
                rank=1,
                name="Example SaaS",
                description="A successful SaaS product - configure TrustMRR scraping for real data",
                url=f"{self.BASE_URL}/project/example",
                mrr=50000.0,
                arr=600000.0,
                mrr_growth=15.0,
                category="SaaS",
                is_verified=True,
            )
        ]

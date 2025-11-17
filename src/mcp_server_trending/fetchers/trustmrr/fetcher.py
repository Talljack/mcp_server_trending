"""TrustMRR fetcher implementation using Playwright for client-side rendering."""

import re

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from ...models import TrendingResponse, TrustMRRProject
from ...utils import logger
from ..base import BaseFetcher


class TrustMRRFetcher(BaseFetcher):
    """Fetcher for TrustMRR revenue rankings using Playwright."""

    BASE_URL = "https://trustmrr.com"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._playwright = None
        self._browser = None

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

    async def _get_browser(self):
        """Get or create Playwright browser instance."""
        if self._browser is None:
            if self._playwright is None:
                self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch()
        return self._browser

    async def _fetch_rankings_internal(self, limit: int = 50) -> TrendingResponse:
        """Internal method to fetch rankings using Playwright."""
        try:
            logger.info("Fetching TrustMRR rankings using Playwright")

            # Get browser
            browser = await self._get_browser()
            page = await browser.new_page()

            try:
                # Navigate to TrustMRR
                await page.goto(self.BASE_URL)

                # Wait for table to load (use attached state instead of visible)
                logger.info("Waiting for TrustMRR table to load")
                await page.wait_for_selector("tr", state="attached", timeout=10000)

                # Wait a bit more for dynamic content
                await page.wait_for_timeout(3000)

                # Get rendered HTML
                content = await page.content()

                # Parse projects
                projects = self._parse_projects(content, limit)

                logger.info(f"Successfully fetched {len(projects)} TrustMRR projects")

                return self._create_response(
                    success=True,
                    data_type="rankings",
                    data=projects,
                    metadata={
                        "total_count": len(projects),
                        "limit": limit,
                        "source": "playwright",
                    },
                )

            finally:
                await page.close()

        except Exception as e:
            logger.error(f"Error fetching TrustMRR rankings: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="rankings",
                data=[],
                error=str(e),
            )

    def _parse_projects(self, html_content: str, limit: int) -> list[TrustMRRProject]:
        """Parse projects from rendered HTML."""
        projects = []

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all table rows
            rows = soup.find_all("tr")

            # Skip header row
            for row in rows[1 : limit + 1]:
                try:
                    cells = row.find_all(["td", "th"])

                    if len(cells) < 4:
                        continue

                    # Extract data from cells
                    # Cell 0: Rank
                    # Cell 1: Name and description
                    # Cell 2: Founder
                    # Cell 3: Revenue
                    # Cell 4: MRR (if available)

                    rank_text = cells[0].get_text(strip=True)
                    # Remove emoji medals
                    rank_text = re.sub(r"[🥇🥈🥉]", "", rank_text).strip()
                    try:
                        rank = int(rank_text) if rank_text else len(projects) + 1
                    except ValueError:
                        rank = len(projects) + 1

                    # Name and description from structured HTML
                    name = "Unknown"
                    description = ""

                    if len(cells) > 1:
                        cell = cells[1]

                        # Try to find name from font-medium div
                        name_div = cell.find("div", class_=lambda x: x and "font-medium" in x)
                        if name_div:
                            name = name_div.get_text(strip=True)
                        else:
                            # Fallback: try img alt attribute
                            img = cell.find("img")
                            if img and img.get("alt"):
                                name = img.get("alt")

                        # Try to find description from text-muted-foreground div
                        desc_div = cell.find(
                            "div", class_=lambda x: x and "text-muted-foreground" in x
                        )
                        if desc_div:
                            description = desc_div.get_text(strip=True)

                    # Founder
                    founder_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                    founders = [founder_text] if founder_text else None

                    # Revenue
                    revenue_text = cells[3].get_text(strip=True) if len(cells) > 3 else "$0"
                    revenue = self._parse_currency(revenue_text)

                    # MRR
                    mrr_text = cells[4].get_text(strip=True) if len(cells) > 4 else "-"
                    mrr = self._parse_currency(mrr_text) if mrr_text != "-" else None

                    # Build URL (using rank for now)
                    url = f"{self.BASE_URL}#{rank}"

                    project = TrustMRRProject(
                        rank=rank,
                        name=name,
                        description=description,
                        url=url,
                        mrr=mrr if mrr is not None else 0.0,  # MRR is required field
                        arr=revenue,  # Total revenue shown as ARR
                        founders=founders,
                        is_verified=True,
                    )

                    projects.append(project)

                except Exception as e:
                    logger.warning(f"Error parsing project row: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing TrustMRR HTML: {e}")

        return projects[:limit]

    def _parse_currency(self, text: str) -> float:
        """Parse currency string to float."""
        try:
            # Remove currency symbols and commas
            cleaned = re.sub(r"[$,]", "", text)
            # Handle K, M, B suffixes
            multiplier = 1
            if "K" in cleaned.upper():
                multiplier = 1000
                cleaned = cleaned.upper().replace("K", "")
            elif "M" in cleaned.upper():
                multiplier = 1000000
                cleaned = cleaned.upper().replace("M", "")
            elif "B" in cleaned.upper():
                multiplier = 1000000000
                cleaned = cleaned.upper().replace("B", "")

            value = float(cleaned) * multiplier
            return value
        except Exception:
            return 0.0

    async def close(self):
        """Close Playwright browser and cleanup."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        # Call parent cleanup
        await super().close()

"""AI Tools Directory fetcher implementation."""

from bs4 import BeautifulSoup

from ...models import AITool, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class AIToolsFetcher(BaseFetcher):
    """Fetcher for AI Tools Directory (There's An AI For That)."""

    BASE_URL = "https://theresanaiforthat.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "aitools"

    async def fetch_trending(
        self,
        category: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending AI tools.

        Args:
            category: Optional category filter
            limit: Number of tools to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with AI tools
        """
        return await self.fetch_with_cache(
            data_type="trending",
            fetch_func=self._fetch_trending_internal,
            use_cache=use_cache,
            category=category,
            limit=limit,
        )

    async def _fetch_trending_internal(
        self, category: str | None = None, limit: int = 50
    ) -> TrendingResponse:
        """Internal method to fetch trending tools."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            # Build URL
            url = self.BASE_URL
            if category:
                url = f"{self.BASE_URL}/category/{category}"

            response = await self.http_client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            tools = self._parse_tools(soup, limit)

            return self._create_response(
                success=True,
                data_type="trending",
                data=tools,
                metadata={
                    "total_count": len(tools),
                    "category": category,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching AI Tools: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending",
                data=[],
                error=str(e),
            )

    def _parse_tools(self, soup: BeautifulSoup, limit: int) -> list[AITool]:
        """Parse AI tools from HTML."""
        tools = []

        # Try to find tool containers
        tool_elements = soup.find_all(["div", "article"], limit=limit * 2)

        for rank, element in enumerate(tool_elements[:limit], 1):
            try:
                tool = self._parse_single_tool(element, rank)
                if tool:
                    tools.append(tool)
            except Exception as e:
                logger.warning(f"Error parsing tool at rank {rank}: {e}")
                continue

        # If parsing fails, return fallback data
        if not tools:
            logger.warning("Failed to parse AI Tools data, using fallback")
            tools = self._get_fallback_tools()

        return tools[:limit]

    def _parse_single_tool(self, element: BeautifulSoup, rank: int) -> AITool | None:
        """Parse a single AI tool."""
        # Try to extract tool info
        name = "AI Tool"
        description = "AI tool description"
        url = f"{self.BASE_URL}/ai/example"
        website = None
        category = None
        tags = []
        pricing = None

        # Try to find name
        name_elem = element.find(["h2", "h3", "a"])
        if name_elem:
            name = name_elem.get_text(strip=True)
            # If it's a link, extract URL
            if name_elem.name == "a" and name_elem.get("href"):
                href = name_elem.get("href")
                if href.startswith("http"):
                    url = href
                elif href.startswith("/"):
                    url = f"{self.BASE_URL}{href}"

        # Try to find description
        desc_elem = element.find("p")
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # Try to find category/tags
        tag_elements = element.find_all(
            ["span", "a"],
            class_=lambda x: x and ("tag" in str(x).lower() or "category" in str(x).lower()),
        )
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
                if not category:
                    category = tag_text

        # Try to find pricing
        pricing_keywords = ["free", "freemium", "paid", "trial"]
        text = element.get_text().lower()
        for keyword in pricing_keywords:
            if keyword in text:
                pricing = keyword.capitalize()
                break

        return AITool(
            rank=rank,
            name=name,
            description=description,
            url=url,
            website=website,
            category=category,
            tags=tags,
            pricing=pricing,
        )

    def _get_fallback_tools(self) -> list[AITool]:
        """Get fallback tools for demonstration."""
        logger.info("Using fallback AI Tools data")
        return [
            AITool(
                rank=1,
                name="Example AI Tool",
                description="An AI tool for demonstration - configure scraping for real data",
                url=f"{self.BASE_URL}/ai/example",
                website="https://example.com",
                category="Productivity",
                tags=["AI", "Productivity", "Automation"],
                pricing="Freemium",
                rating=4.5,
                reviews_count=100,
                is_featured=True,
            )
        ]

    async def fetch_by_category(
        self, category: str, limit: int = 50, use_cache: bool = True
    ) -> TrendingResponse:
        """Convenience method to fetch tools by category."""
        return await self.fetch_trending(category=category, limit=limit, use_cache=use_cache)

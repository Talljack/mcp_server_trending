"""Papers with Code fetcher implementation.

Papers with Code / HuggingFace Daily Papers - trending ML papers with code.

Note: Papers with Code API doesn't work well, so we use HuggingFace Daily Papers API
which provides similar trending ML papers data.

API: https://huggingface.co/api/daily_papers
- Public API, no authentication required
"""

from datetime import datetime

from ...models import TrendingResponse
from ...models.paperswithcode import PapersWithCodePaper
from ...utils import logger
from ..base import BaseFetcher


class PapersWithCodeFetcher(BaseFetcher):
    """Fetcher for trending ML papers (via HuggingFace Daily Papers)."""

    def __init__(self, **kwargs):
        """Initialize Papers with Code fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://huggingface.co"
        self.api_url = "https://huggingface.co/api/daily_papers"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "paperswithcode"

    async def fetch_trending_papers(
        self,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending papers from HuggingFace Daily Papers.

        Args:
            limit: Number of papers to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with trending papers
        """
        return await self.fetch_with_cache(
            data_type="trending_papers",
            fetch_func=self._fetch_trending_papers_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_trending_papers_internal(self, limit: int = 50) -> TrendingResponse:
        """Internal implementation to fetch trending papers."""
        try:
            url = self.api_url
            params = {"limit": limit}
            logger.info(f"Fetching trending papers from {url}")

            response = await self.http_client.get(url, params=params)
            data = response.json()

            papers = self._parse_papers(data, limit)

            return self._create_response(
                success=True,
                data_type="trending_papers",
                data=papers,
                metadata={
                    "total_count": len(papers),
                    "limit": limit,
                    "source": "huggingface.co/papers",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching trending papers: {e}")
            return self._create_response(
                success=False,
                data_type="trending_papers",
                data=[],
                error=str(e),
            )

    async def fetch_latest_papers(
        self,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch latest papers (same as trending for HuggingFace API).

        Args:
            limit: Number of papers to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with latest papers
        """
        return await self.fetch_with_cache(
            data_type="latest_papers",
            fetch_func=self._fetch_latest_papers_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_latest_papers_internal(self, limit: int = 50) -> TrendingResponse:
        """Internal implementation to fetch latest papers."""
        try:
            url = self.api_url
            params = {"limit": limit}
            logger.info(f"Fetching latest papers from {url}")

            response = await self.http_client.get(url, params=params)
            data = response.json()

            papers = self._parse_papers(data, limit)

            return self._create_response(
                success=True,
                data_type="latest_papers",
                data=papers,
                metadata={
                    "total_count": len(papers),
                    "limit": limit,
                    "source": "huggingface.co/papers",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching latest papers: {e}")
            return self._create_response(
                success=False,
                data_type="latest_papers",
                data=[],
                error=str(e),
            )

    async def search_papers(
        self,
        query: str,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Search papers (filters from daily papers by keyword).

        Args:
            query: Search query
            limit: Number of papers to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with search results
        """
        return await self.fetch_with_cache(
            data_type=f"search_{query}",
            fetch_func=self._search_papers_internal,
            use_cache=use_cache,
            query=query,
            limit=min(limit, 100),
        )

    async def _search_papers_internal(self, query: str, limit: int = 50) -> TrendingResponse:
        """Internal implementation to search papers."""
        try:
            # Fetch more papers and filter by query
            url = self.api_url
            params = {"limit": 100}  # Fetch more to filter (max 100)
            logger.info(f"Searching papers for '{query}'")

            response = await self.http_client.get(url, params=params)
            data = response.json()

            # Filter papers by query in title, summary, or keywords
            query_lower = query.lower()
            filtered_data = []
            for item in data:
                paper = item.get("paper", {})
                title = paper.get("title", "").lower()
                summary = paper.get("summary", "").lower()
                keywords = paper.get("ai_keywords", []) or []
                keywords_str = " ".join(keywords).lower()

                if query_lower in title or query_lower in summary or query_lower in keywords_str:
                    filtered_data.append(item)

            papers = self._parse_papers(filtered_data, limit)

            return self._create_response(
                success=True,
                data_type=f"search_{query}",
                data=papers,
                metadata={
                    "query": query,
                    "total_count": len(papers),
                    "limit": limit,
                    "source": "huggingface.co/papers",
                },
            )

        except Exception as e:
            logger.error(f"Error searching papers for '{query}': {e}")
            return self._create_response(
                success=False,
                data_type=f"search_{query}",
                data=[],
                error=str(e),
            )

    def _parse_papers(self, data: list, limit: int) -> list[PapersWithCodePaper]:
        """Parse papers from HuggingFace Daily Papers API response."""
        papers = []

        for i, item in enumerate(data[:limit]):
            try:
                paper = item.get("paper", {})

                # Parse published date
                published_str = paper.get("publishedAt") or item.get("publishedAt")
                published = None
                if published_str:
                    try:
                        published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        pass

                # Extract authors
                authors = []
                for author in paper.get("authors", []):
                    name = author.get("name", "")
                    if name and not author.get("hidden", False):
                        authors.append(name)

                # Get arxiv ID and URLs
                arxiv_id = paper.get("id", "")

                paper_obj = PapersWithCodePaper(
                    rank=i + 1,
                    id=arxiv_id,
                    title=paper.get("title", "") or item.get("title", ""),
                    abstract=paper.get("summary", "") or item.get("summary", "") or "",
                    url_abs=f"https://huggingface.co/papers/{arxiv_id}" if arxiv_id else "",
                    url_pdf=f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else "",
                    arxiv_id=arxiv_id,
                    published=published,
                    authors=authors,
                    tasks=paper.get("ai_keywords", []) or [],
                    methods=[],
                    repository_url=paper.get("githubRepo", "") or "",
                    stars=paper.get("githubStars", 0) or 0,
                )
                papers.append(paper_obj)

            except Exception as e:
                logger.warning(f"Error parsing paper: {e}")
                continue

        return papers

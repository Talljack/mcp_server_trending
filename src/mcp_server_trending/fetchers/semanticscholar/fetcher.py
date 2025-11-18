"""Semantic Scholar fetcher implementation."""

from ...models.base import TrendingResponse
from ...models.semanticscholar import SemanticScholarAuthor, SemanticScholarPaper
from ...utils import logger
from ..base import BaseFetcher


class SemanticScholarFetcher(BaseFetcher):
    """
    Fetcher for Semantic Scholar research papers.

    Uses the official Semantic Scholar API: https://api.semanticscholar.org
    API Documentation: https://api.semanticscholar.org/api-docs/

    Features:
    - Search papers by keywords
    - Filter by fields of study
    - Sort by citations or publication date
    - Get influential citation counts
    - Access open access PDFs

    Popular fields of study:
    - Computer Science
    - Medicine
    - Biology
    - Physics
    - Mathematics
    - Chemistry
    - Engineering

    Rate limits:
    - Public API: 100 requests per 5 minutes (1 req/3s recommended)
    - With API Key: 5,000 requests per 5 minutes

    Recommendation: Get free API key from https://www.semanticscholar.org/product/api#api-key
    """

    API_BASE = "https://api.semanticscholar.org/graph/v1"

    # Paper fields to request
    PAPER_FIELDS = [
        "paperId",
        "title",
        "abstract",
        "authors",
        "year",
        "citationCount",
        "influentialCitationCount",
        "venue",
        "publicationDate",
        "url",
        "isOpenAccess",
        "openAccessPdf",
        "fieldsOfStudy",
    ]

    def __init__(self, cache=None, http_client=None, cache_ttl=3600, api_key=None):
        """
        Initialize Semantic Scholar fetcher.

        Args:
            cache: Cache instance
            http_client: HTTP client instance
            cache_ttl: Cache TTL in seconds (default: 1 hour)
            api_key: Optional Semantic Scholar API key for higher rate limits
        """
        super().__init__(cache, http_client, cache_ttl)
        self.api_key = api_key

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "semanticscholar"

    async def search_papers(
        self,
        query: str | None = None,
        fields_of_study: list[str] | None = None,
        year: str | None = None,
        venue: str | None = None,
        min_citation_count: int | None = None,
        open_access_pdf: bool = False,
        sort: str = "citationCount:desc",
        limit: int = 100,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Search Semantic Scholar papers.

        Args:
            query: Search query string
            fields_of_study: Filter by fields (e.g., ['Computer Science', 'Medicine'])
            year: Year range (e.g., '2020-2023', '2023')
            venue: Conference/journal name
            min_citation_count: Minimum citation count
            open_access_pdf: Only papers with open access PDFs
            sort: Sort order (citationCount:desc, publicationDate:desc, relevance)
            limit: Number of papers (max 100 per request)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with paper data
        """
        return await self.fetch_with_cache(
            data_type="papers",
            fetch_func=self._search_papers_internal,
            use_cache=use_cache,
            query=query,
            fields_of_study=fields_of_study,
            year=year,
            venue=venue,
            min_citation_count=min_citation_count,
            open_access_pdf=open_access_pdf,
            sort=sort,
            limit=limit,
        )

    async def _search_papers_internal(
        self,
        query: str | None = None,
        fields_of_study: list[str] | None = None,
        year: str | None = None,
        venue: str | None = None,
        min_citation_count: int | None = None,
        open_access_pdf: bool = False,
        sort: str = "citationCount:desc",
        limit: int = 100,
    ) -> TrendingResponse:
        """Internal method to search papers."""
        try:
            # Default to recent CS papers if no query
            if not query:
                query = "computer science"

            # Build API request parameters
            params = {
                "query": query,
                "fields": ",".join(self.PAPER_FIELDS),
                "limit": min(limit, 100),  # API max is 100
            }

            # Add optional filters
            if fields_of_study:
                params["fieldsOfStudy"] = ",".join(fields_of_study)

            if year:
                params["year"] = year

            if venue:
                params["venue"] = venue

            if min_citation_count is not None:
                params["minCitationCount"] = min_citation_count

            if open_access_pdf:
                params["openAccessPdf"] = ""

            # Sort parameter
            if sort:
                params["sort"] = sort

            logger.info(f"Searching Semantic Scholar with query: {query}")

            # Prepare headers with API key if available
            headers = {}
            if self.api_key:
                headers["x-api-key"] = self.api_key
                logger.debug("Using Semantic Scholar API key for higher rate limits")

            # Make request
            url = f"{self.API_BASE}/paper/search"
            response = await self.http_client.get(url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()

            # Parse papers
            papers = self._parse_papers(data.get("data", []))

            metadata = {
                "total_count": len(papers),
                "total_results": data.get("total", 0),
                "query": query,
                "fields_of_study": fields_of_study,
                "year": year,
                "venue": venue,
                "min_citation_count": min_citation_count,
                "open_access_only": open_access_pdf,
                "sort": sort,
                "limit": limit,
                "url": "https://www.semanticscholar.org/",
                "data_source": "Semantic Scholar API",
                "api_key_used": bool(self.api_key),
            }

            return self._create_response(
                success=True,
                data_type="papers",
                data=papers,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error searching Semantic Scholar: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="papers",
                data=[],
                error=str(e),
            )

    def _parse_papers(self, papers_data: list) -> list[SemanticScholarPaper]:
        """Parse papers from API response."""
        papers = []

        for rank, paper_data in enumerate(papers_data, 1):
            try:
                # Extract authors
                authors = []
                authors_data = paper_data.get("authors", [])
                for author_data in authors_data:
                    author = SemanticScholarAuthor(
                        author_id=author_data.get("authorId"),
                        name=author_data.get("name", ""),
                    )
                    authors.append(author)

                # Extract fields of study
                fields_of_study = paper_data.get("fieldsOfStudy") or []

                # Open access PDF
                open_access_pdf = None
                if paper_data.get("openAccessPdf"):
                    open_access_pdf = paper_data["openAccessPdf"].get("url")

                # Build paper URL
                paper_id = paper_data.get("paperId", "")
                url = paper_data.get("url", f"https://www.semanticscholar.org/paper/{paper_id}")

                paper = SemanticScholarPaper(
                    rank=rank,
                    paper_id=paper_id,
                    title=paper_data.get("title", ""),
                    abstract=paper_data.get("abstract"),
                    authors=authors,
                    year=paper_data.get("year"),
                    citation_count=paper_data.get("citationCount", 0),
                    influential_citation_count=paper_data.get("influentialCitationCount", 0),
                    venue=paper_data.get("venue"),
                    publication_date=paper_data.get("publicationDate"),
                    url=url,
                    is_open_access=paper_data.get("isOpenAccess", False),
                    open_access_pdf=open_access_pdf,
                    fields_of_study=fields_of_study,
                )

                papers.append(paper)

            except Exception as e:
                logger.warning(f"Error parsing Semantic Scholar paper: {e}")
                continue

        logger.info(f"Successfully parsed {len(papers)} Semantic Scholar papers")

        return papers

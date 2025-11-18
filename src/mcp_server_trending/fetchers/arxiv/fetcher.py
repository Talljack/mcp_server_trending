"""arXiv fetcher implementation."""

import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

from ...models.arxiv import ArxivPaper
from ...models.base import TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class ArxivFetcher(BaseFetcher):
    """
    Fetcher for arXiv research papers.

    Uses the official arXiv API: http://export.arxiv.org/api/query
    API Documentation: https://info.arxiv.org/help/api/index.html

    Features:
    - Search by category (cs.AI, cs.LG, math.NA, etc.)
    - Search by keywords
    - Sort by submission date, update date, or relevance
    - Get recent papers

    Popular categories:
    - cs.AI: Artificial Intelligence
    - cs.LG: Machine Learning
    - cs.CL: Computation and Language (NLP)
    - cs.CV: Computer Vision
    - cs.CR: Cryptography and Security
    - stat.ML: Statistics - Machine Learning
    - math.NA: Numerical Analysis
    - physics.comp-ph: Computational Physics
    """

    API_URL = "http://export.arxiv.org/api/query"

    # Namespaces for XML parsing
    NAMESPACES = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "arxiv"

    async def fetch_papers(
        self,
        category: str | None = None,
        search_query: str | None = None,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch arXiv papers.

        Args:
            category: arXiv category (e.g., cs.AI, cs.LG, cs.CV)
            search_query: Search keywords
            sort_by: Sort field (submittedDate, lastUpdatedDate, relevance)
            sort_order: Sort order (ascending, descending)
            limit: Number of papers to fetch (max 2000)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with paper data
        """
        return await self.fetch_with_cache(
            data_type="papers",
            fetch_func=self._fetch_papers_internal,
            use_cache=use_cache,
            category=category,
            search_query=search_query,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
        )

    async def _fetch_papers_internal(
        self,
        category: str | None = None,
        search_query: str | None = None,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch papers."""
        try:
            # Build search query
            search_parts = []

            if category:
                # Search by category
                search_parts.append(f"cat:{category}")

            if search_query:
                # Add keyword search
                if search_parts:
                    search_parts.append(f"AND all:{search_query}")
                else:
                    search_parts.append(f"all:{search_query}")

            # Default to recent CS papers if no query specified
            if not search_parts:
                search_parts.append("cat:cs.*")

            query = " ".join(search_parts)

            # Build API request parameters
            params = {
                "search_query": query,
                "start": 0,
                "max_results": min(limit, 2000),  # API max is 2000
                "sortBy": sort_by,
                "sortOrder": sort_order,
            }

            logger.info(f"Fetching arXiv papers with query: {query}")

            # Make request
            response = await self.http_client.get(self.API_URL, params=params)
            response.raise_for_status()

            # Parse XML response
            papers = self._parse_papers(response.text)

            metadata = {
                "total_count": len(papers),
                "category": category,
                "search_query": search_query,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "limit": limit,
                "url": "https://arxiv.org/",
                "data_source": "arXiv API",
            }

            return self._create_response(
                success=True,
                data_type="papers",
                data=papers,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching arXiv papers: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="papers",
                data=[],
                error=str(e),
            )

    def _parse_papers(self, xml_text: str) -> list[ArxivPaper]:
        """Parse papers from arXiv API XML response."""
        papers = []

        try:
            root = ET.fromstring(xml_text)

            # Find all entry elements
            entries = root.findall("atom:entry", self.NAMESPACES)

            for rank, entry in enumerate(entries, 1):
                try:
                    # Extract paper data
                    arxiv_id = self._get_text(entry, "atom:id").split("/abs/")[-1]
                    title = self._get_text(entry, "atom:title").strip()
                    summary = self._get_text(entry, "atom:summary").strip()
                    published = self._get_text(entry, "atom:published")
                    updated = self._get_text(entry, "atom:updated")

                    # Extract authors
                    authors = []
                    author_elements = entry.findall("atom:author", self.NAMESPACES)
                    for author_elem in author_elements:
                        name = self._get_text(author_elem, "atom:name")
                        if name:
                            authors.append(name)

                    # Extract categories
                    categories = []
                    primary_category = ""
                    category_elements = entry.findall("atom:category", self.NAMESPACES)
                    for i, cat_elem in enumerate(category_elements):
                        cat_term = cat_elem.get("term", "")
                        if cat_term:
                            categories.append(cat_term)
                            if i == 0:
                                primary_category = cat_term

                    # Primary category from arxiv:primary_category element
                    primary_cat_elem = entry.find("arxiv:primary_category", self.NAMESPACES)
                    if primary_cat_elem is not None:
                        primary_category = primary_cat_elem.get("term", primary_category)

                    # Optional fields
                    comment = self._get_text(entry, "arxiv:comment") or None
                    journal_ref = self._get_text(entry, "arxiv:journal_ref") or None
                    doi = self._get_text(entry, "arxiv:doi") or None

                    # Build URLs
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    abs_url = f"https://arxiv.org/abs/{arxiv_id}"

                    paper = ArxivPaper(
                        rank=rank,
                        arxiv_id=arxiv_id,
                        title=title,
                        authors=authors,
                        summary=summary,
                        published=published,
                        updated=updated,
                        categories=categories,
                        primary_category=primary_category,
                        pdf_url=pdf_url,
                        abs_url=abs_url,
                        comment=comment,
                        journal_ref=journal_ref,
                        doi=doi,
                    )

                    papers.append(paper)

                except Exception as e:
                    logger.warning(f"Error parsing arXiv paper entry: {e}")
                    continue

            logger.info(f"Successfully parsed {len(papers)} arXiv papers")

        except Exception as e:
            logger.error(f"Error parsing arXiv XML: {e}", exc_info=True)

        return papers

    def _get_text(self, element: ET.Element, path: str) -> str:
        """Safely get text from XML element."""
        child = element.find(path, self.NAMESPACES)
        if child is not None and child.text:
            return child.text.strip()
        return ""

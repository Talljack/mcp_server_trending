"""OpenReview fetcher implementation."""

import urllib.parse

from ...models.base import TrendingResponse
from ...models.openreview import OpenReviewPaper
from ...utils import logger
from ..base import BaseFetcher


class OpenReviewFetcher(BaseFetcher):
    """
    Fetcher for OpenReview conference papers.

    Uses the official OpenReview API v2: https://api2.openreview.net
    API Documentation: https://docs.openreview.net/reference/api-v2

    Features:
    - Get papers from ML conferences (NeurIPS, ICLR, ICML, etc.)
    - Access peer review scores and decisions
    - Filter by acceptance status
    - Sort by rating or submission date

    Popular venues:
    - ICLR.cc/2024/Conference (ICLR 2024)
    - NeurIPS.cc/2023/Conference (NeurIPS 2023)
    - ICML.cc/2024/Conference (ICML 2024)
    - AAAI.org/2024/Conference (AAAI 2024)

    Note: OpenReview API has rate limits. Use cache for frequent requests.
    """

    API_BASE = "https://api2.openreview.net"

    # Common venue patterns
    VENUES = {
        "iclr2024": "ICLR.cc/2024/Conference",
        "iclr2023": "ICLR.cc/2023/Conference",
        "neurips2023": "NeurIPS.cc/2023/Conference",
        "neurips2022": "NeurIPS.cc/2022/Conference",
        "icml2024": "ICML.cc/2024/Conference",
        "icml2023": "ICML.cc/2023/Conference",
    }

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "openreview"

    async def fetch_papers(
        self,
        venue: str = "ICLR.cc/2024/Conference",
        content: str | None = None,
        decision: str | None = None,
        limit: int = 100,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch OpenReview conference papers.

        Args:
            venue: Venue identifier (e.g., 'ICLR.cc/2024/Conference' or shorthand 'iclr2024')
            content: Search in title/abstract
            decision: Filter by decision (Accept, Reject)
            limit: Number of papers (max 1000)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with paper data
        """
        return await self.fetch_with_cache(
            data_type="papers",
            fetch_func=self._fetch_papers_internal,
            use_cache=use_cache,
            venue=venue,
            content=content,
            decision=decision,
            limit=limit,
        )

    async def _fetch_papers_internal(
        self,
        venue: str = "ICLR.cc/2024/Conference",
        content: str | None = None,
        decision: str | None = None,
        limit: int = 100,
    ) -> TrendingResponse:
        """Internal method to fetch papers."""
        try:
            # Convert shorthand to full venue name
            venue_id = self.VENUES.get(venue.lower(), venue)

            # Build invitation for submissions
            invitation = f"{venue_id}/-/Submission"

            # Build API request parameters
            params = {
                "invitation": invitation,
                "details": "replies,original",  # Get reviews and original submission
                "limit": min(limit, 1000),  # API supports up to 1000
                "offset": 0,
            }

            # Add content search if specified
            if content:
                params["content"] = {"title": content}

            logger.info(f"Fetching OpenReview papers from venue: {venue_id}")

            # Make request
            url = f"{self.API_BASE}/notes"
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            # Parse papers
            papers = self._parse_papers(data.get("notes", []), venue_id)

            # Filter by decision if specified
            if decision:
                papers = [
                    p for p in papers if p.decision and decision.lower() in p.decision.lower()
                ]

            # Limit results
            papers = papers[:limit]

            metadata = {
                "total_count": len(papers),
                "venue": venue_id,
                "content_search": content,
                "decision_filter": decision,
                "limit": limit,
                "url": "https://openreview.net/",
                "data_source": "OpenReview API",
            }

            return self._create_response(
                success=True,
                data_type="papers",
                data=papers,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching OpenReview papers: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="papers",
                data=[],
                error=str(e),
            )

    def _parse_papers(self, notes_data: list, venue: str) -> list[OpenReviewPaper]:
        """Parse papers from API response."""
        papers = []

        for rank, note in enumerate(notes_data, 1):
            try:
                content = note.get("content", {})

                # Extract basic info
                paper_id = note.get("id", "")
                title = content.get("title", {})
                if isinstance(title, dict):
                    title = title.get("value", "")

                abstract = content.get("abstract", {})
                if isinstance(abstract, dict):
                    abstract = abstract.get("value")

                # Extract authors
                authors_data = content.get("authors", {})
                if isinstance(authors_data, dict):
                    authors_data = authors_data.get("value", [])
                authors = [str(a) for a in authors_data] if authors_data else []

                # Extract keywords
                keywords_data = content.get("keywords", {})
                if isinstance(keywords_data, dict):
                    keywords_data = keywords_data.get("value", [])
                keywords = [str(k) for k in keywords_data] if keywords_data else []

                # Extract decision from details/replies
                decision = None
                details = note.get("details", {})
                replies = details.get("replies", [])
                for reply in replies:
                    reply_content = reply.get("content", {})
                    if "decision" in reply_content:
                        decision_data = reply_content["decision"]
                        if isinstance(decision_data, dict):
                            decision = decision_data.get("value")
                        else:
                            decision = str(decision_data)
                        break

                # Extract ratings from reviews
                ratings = []
                confidences = []
                for reply in replies:
                    reply_content = reply.get("content", {})

                    # Extract rating
                    if "rating" in reply_content:
                        rating_data = reply_content["rating"]
                        if isinstance(rating_data, dict):
                            rating_value = rating_data.get("value")
                        else:
                            rating_value = rating_data

                        # Parse rating (usually like "7: Good paper")
                        if rating_value:
                            try:
                                rating_str = str(rating_value).split(":")[0].strip()
                                ratings.append(float(rating_str))
                            except (ValueError, IndexError):
                                pass

                    # Extract confidence
                    if "confidence" in reply_content:
                        conf_data = reply_content["confidence"]
                        if isinstance(conf_data, dict):
                            conf_value = conf_data.get("value")
                        else:
                            conf_value = conf_data

                        if conf_value:
                            try:
                                conf_str = str(conf_value).split(":")[0].strip()
                                confidences.append(float(conf_str))
                            except (ValueError, IndexError):
                                pass

                # Calculate average rating and confidence
                rating = sum(ratings) / len(ratings) if ratings else None
                confidence = sum(confidences) / len(confidences) if confidences else None

                # Build URLs
                forum_url = f"https://openreview.net/forum?id={paper_id}"

                # PDF URL (if available)
                pdf_url = None
                pdf_data = content.get("pdf")
                if pdf_data:
                    if isinstance(pdf_data, dict):
                        pdf_url = pdf_data.get("value")
                    else:
                        pdf_url = str(pdf_data)

                    # Construct full URL if needed
                    if pdf_url and not pdf_url.startswith("http"):
                        pdf_url = f"https://openreview.net{pdf_url}"

                # Submission date
                submission_date = None
                cdate = note.get("cdate")
                if cdate:
                    # Convert timestamp to ISO format
                    from datetime import datetime

                    submission_date = datetime.fromtimestamp(cdate / 1000).isoformat()

                paper = OpenReviewPaper(
                    rank=rank,
                    paper_id=paper_id,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    keywords=keywords,
                    venue=venue,
                    decision=decision,
                    rating=rating,
                    confidence=confidence,
                    pdf_url=pdf_url,
                    forum_url=forum_url,
                    submission_date=submission_date,
                )

                papers.append(paper)

            except Exception as e:
                logger.warning(f"Error parsing OpenReview paper: {e}")
                continue

        logger.info(f"Successfully parsed {len(papers)} OpenReview papers")

        return papers

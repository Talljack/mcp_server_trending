"""arXiv data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class ArxivPaper(BaseModel):
    """arXiv research paper."""

    rank: int
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: str
    updated: str
    categories: list[str]
    primary_category: str
    pdf_url: str
    abs_url: str
    comment: str | None = None
    journal_ref: str | None = None
    doi: str | None = None


@dataclass
class ArxivQuery:
    """Parameters for arXiv queries."""

    category: str | None = None  # cs.AI, cs.LG, math.NA, etc.
    search_query: str | None = None  # Search keywords
    sort_by: str = "submittedDate"  # submittedDate, lastUpdatedDate, relevance
    sort_order: str = "descending"  # ascending, descending
    max_results: int = 50

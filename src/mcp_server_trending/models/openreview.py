"""OpenReview data models."""

from dataclasses import dataclass, field

from .base import BaseModel


@dataclass
class OpenReviewPaper(BaseModel):
    """OpenReview conference paper."""

    rank: int
    paper_id: str
    title: str
    abstract: str | None
    authors: list[str]
    keywords: list[str]
    venue: str  # e.g., "ICLR 2024", "NeurIPS 2023"
    decision: str | None  # Accept/Reject/Pending
    rating: float | None  # Average rating score
    confidence: float | None  # Average reviewer confidence
    pdf_url: str | None
    forum_url: str
    submission_date: str | None


@dataclass
class OpenReviewQuery:
    """Parameters for OpenReview queries."""

    venue: str = "ICLR.cc/2024/Conference"  # Venue identifier
    content: str | None = None  # Search in title/abstract
    decision: str | None = None  # Filter by decision (Accept, Reject)
    min_rating: float | None = None  # Minimum rating
    sort: str = "cdate"  # Sort by: cdate (creation date), rating
    limit: int = 100

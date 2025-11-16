"""Indie Hackers data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class IndieHackersPost(BaseModel):
    """Indie Hackers post model."""

    rank: int
    id: str
    title: str
    url: str
    author: str
    author_url: str
    content_preview: str
    upvotes: int
    comments_count: int
    created_at: datetime
    post_type: str  # "post", "milestone", "income_report"
    tags: list[str] = field(default_factory=list)
    thumbnail_url: str | None = None


@dataclass
class IncomeReport(BaseModel):
    """Indie Hackers income report model."""

    rank: int
    project_name: str
    project_url: str
    author: str
    author_url: str
    revenue: str  # e.g., "$10,000/mo", "$120k/year"
    revenue_amount: float | None = None  # Parsed amount
    revenue_period: str | None = None  # "monthly" or "yearly"
    description: str = ""
    created_at: datetime | None = None
    upvotes: int = 0
    comments_count: int = 0


@dataclass
class ProjectMilestone(BaseModel):
    """Indie Hackers project milestone model."""

    rank: int
    project_name: str
    project_url: str
    author: str
    author_url: str
    milestone_type: str  # e.g., "First Dollar", "$1K MRR", "10K Users"
    milestone_value: str
    description: str
    achieved_at: datetime
    upvotes: int = 0
    comments_count: int = 0

"""Stack Overflow data models."""

from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass
class StackOverflowTag(BaseModel):
    """Stack Overflow tag."""

    rank: int
    name: str
    count: int  # Number of questions with this tag
    has_synonyms: bool
    is_moderator_only: bool
    is_required: bool
    url: str  # Tag page URL
    last_activity_date: datetime | None  # Last activity date


@dataclass
class StackOverflowParams:
    """Parameters for Stack Overflow queries."""

    sort: str = "popular"  # popular, activity, name
    order: str = "desc"  # desc, asc
    limit: int = 30  # Number of tags to fetch
    site: str = "stackoverflow"  # Site name


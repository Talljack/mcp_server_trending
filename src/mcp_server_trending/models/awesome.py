"""Awesome Lists data models."""

from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass
class AwesomeList(BaseModel):
    """Awesome list repository."""

    rank: int
    name: str
    full_name: str  # owner/repo
    description: str
    url: str  # GitHub URL
    stars: int
    forks: int
    language: str | None
    updated_at: datetime | None
    created_at: datetime | None
    topics: list[str]  # Repository topics
    owner: str  # Repository owner
    homepage: str | None  # Homepage URL


@dataclass
class AwesomeParams:
    """Parameters for Awesome Lists queries."""

    sort: str = "stars"  # stars, forks, updated
    order: str = "desc"  # desc, asc
    limit: int = 30  # Number of repos to fetch
    language: str | None = None  # Filter by language


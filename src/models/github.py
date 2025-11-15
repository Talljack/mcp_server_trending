"""GitHub data models."""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel


@dataclass
class GitHubDeveloper(BaseModel):
    """GitHub trending developer."""

    rank: int
    username: str
    name: str
    url: str
    avatar: str
    repo_name: Optional[str] = None
    repo_description: Optional[str] = None


@dataclass
class GitHubRepository(BaseModel):
    """GitHub trending repository."""

    rank: int
    author: str
    name: str
    url: str
    description: str
    stars: int
    forks: int
    stars_today: int
    language: Optional[str] = None
    language_color: Optional[str] = None
    built_by: List[str] = field(default_factory=list)


@dataclass
class GitHubTrendingParams:
    """Parameters for GitHub trending queries."""

    time_range: str = "daily"  # daily, weekly, monthly
    language: Optional[str] = None
    spoken_language: Optional[str] = None

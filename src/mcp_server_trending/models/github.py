"""GitHub data models."""

from dataclasses import dataclass, field

from .base import BaseModel


@dataclass
class GitHubDeveloper(BaseModel):
    """GitHub trending developer."""

    rank: int
    username: str
    name: str
    url: str
    avatar: str
    repo_name: str | None = None
    repo_description: str | None = None


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
    language: str | None = None
    language_color: str | None = None
    built_by: list[str] = field(default_factory=list)


@dataclass
class GitHubTrendingParams:
    """Parameters for GitHub trending queries."""

    time_range: str = "daily"  # daily, weekly, monthly
    language: str | None = None
    spoken_language: str | None = None

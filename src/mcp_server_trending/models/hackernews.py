"""Hacker News data models."""

from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass
class HackerNewsStory(BaseModel):
    """Hacker News story."""

    rank: int
    id: int
    title: str
    url: str | None  # Can be None for Ask HN, etc.
    score: int
    author: str
    time: datetime
    descendants: int  # Number of comments
    story_type: str  # story, ask, show, job, poll


@dataclass
class HackerNewsParams:
    """Parameters for Hacker News queries."""

    story_type: str = "top"  # top, best, new, ask, show, job
    limit: int = 30  # Number of stories to fetch

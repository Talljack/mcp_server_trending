"""Hashnode data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class HashnodeAuthor(BaseModel):
    """Hashnode article author information."""

    username: str
    name: str | None = None
    profile_picture: str | None = None
    bio: str | None = None


@dataclass
class HashnodeArticle(BaseModel):
    """Hashnode article/post."""

    rank: int
    id: str
    title: str
    url: str
    slug: str
    brief: str | None = None
    content_markdown: str | None = None
    cover_image: str | None = None

    # Author info
    author: HashnodeAuthor | None = None

    # Engagement metrics
    views: int = 0
    reactions: int = 0
    comments_count: int = 0
    reading_time_minutes: int = 0

    # Tags
    tags: list[str] = field(default_factory=list)

    # Publication info
    publication_id: str | None = None
    publication_name: str | None = None

    # Timestamps
    published_at: datetime | None = None
    updated_at: datetime | None = None

    # Social
    is_featured: bool = False
    is_pinned: bool = False

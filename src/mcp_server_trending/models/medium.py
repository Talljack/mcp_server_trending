"""Medium data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class MediumAuthor(BaseModel):
    """Medium article author information."""

    user_id: str
    username: str
    name: str | None = None
    bio: str | None = None
    image_url: str | None = None
    profile_url: str | None = None


@dataclass
class MediumArticle(BaseModel):
    """Medium article/story."""

    rank: int
    id: str
    title: str
    url: str
    subtitle: str | None = None

    # Author info
    author: MediumAuthor | None = None

    # Preview
    preview_image: str | None = None

    # Engagement metrics
    claps: int = 0
    responses: int = 0
    reading_time_minutes: int = 0

    # Tags
    tags: list[str] = field(default_factory=list)

    # Publication info
    publication_id: str | None = None
    publication_name: str | None = None

    # Content
    unique_slug: str | None = None
    word_count: int = 0

    # Timestamps
    published_at: datetime | None = None
    first_published_at: datetime | None = None
    updated_at: datetime | None = None

    # Premium content
    is_premium: bool = False
    is_locked: bool = False

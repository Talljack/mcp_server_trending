"""dev.to data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class DevToArticle(BaseModel):
    """dev.to article/post."""

    rank: int
    id: int
    title: str
    url: str
    description: str | None = None
    cover_image: str | None = None

    # Author info
    user_id: int | None = None
    user_name: str | None = None
    user_username: str | None = None
    user_profile_image: str | None = None

    # Organization info
    organization_id: int | None = None
    organization_name: str | None = None
    organization_username: str | None = None

    # Tags
    tags: list[str] = field(default_factory=list)
    tag_list: list[str] = field(default_factory=list)

    # Engagement metrics
    positive_reactions_count: int = 0
    public_reactions_count: int = 0
    comments_count: int = 0
    reading_time_minutes: int = 0

    # Type
    type_of: str = "article"  # article, discussion, etc.

    # Timestamps
    published_at: datetime | None = None
    created_at: datetime | None = None
    edited_at: datetime | None = None
    last_comment_at: datetime | None = None

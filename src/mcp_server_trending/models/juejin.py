"""Juejin (掘金) data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class JuejinArticle(BaseModel):
    """Juejin article/post."""

    rank: int
    article_id: str
    title: str
    url: str
    brief_content: str | None = None
    cover_image: str | None = None

    # Author info
    user_id: str | None = None
    user_name: str | None = None
    avatar_large: str | None = None

    # Category and tags
    category_name: str | None = None
    tags: list[str] = field(default_factory=list)

    # Engagement metrics
    view_count: int = 0
    digg_count: int = 0  # 点赞数
    comment_count: int = 0
    collect_count: int = 0  # 收藏数

    # Timestamps
    created_at: datetime | None = None
    published_at: datetime | None = None

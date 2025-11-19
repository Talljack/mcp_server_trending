"""CodePen data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class CodePenUser(BaseModel):
    """CodePen user information."""

    username: str
    name: str | None = None
    avatar: str | None = None
    profile_url: str | None = None


@dataclass
class CodePenPen(BaseModel):
    """CodePen pen/code snippet."""

    rank: int
    id: str
    title: str
    url: str
    description: str | None = None

    # Author info
    user: CodePenUser | None = None

    # Preview
    image_url: str | None = None
    screenshot_url: str | None = None

    # Engagement metrics
    views: int = 0
    loves: int = 0
    comments: int = 0
    forks: int = 0

    # Tags
    tags: list[str] = field(default_factory=list)

    # Content type
    is_private: bool = False
    has_html: bool = False
    has_css: bool = False
    has_js: bool = False

    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None

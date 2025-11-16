"""V2EX data models."""

from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass
class V2EXTopic(BaseModel):
    """V2EX topic/post."""

    rank: int
    id: int
    title: str
    url: str
    content: str | None = None
    content_rendered: str | None = None

    # Author info
    member_id: int | None = None
    member_username: str | None = None
    member_avatar: str | None = None

    # Node (category) info
    node_id: int | None = None
    node_name: str | None = None
    node_title: str | None = None

    # Engagement metrics
    replies: int = 0
    last_reply_time: datetime | None = None
    created: datetime | None = None
    last_modified: datetime | None = None

    # Additional info
    clicks: int = 0

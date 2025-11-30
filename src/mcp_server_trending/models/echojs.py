"""Echo JS data models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EchoJSNews:
    """Echo JS news item data model."""

    rank: int
    id: str
    title: str
    url: str
    created_at: datetime
    up: int  # upvotes
    down: int  # downvotes
    comments: int
    username: str
    ctime: int  # creation timestamp

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "upvotes": self.up,
            "downvotes": self.down,
            "comments": self.comments,
            "username": self.username,
            "score": self.up - self.down,
        }

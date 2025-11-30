"""Lobsters data models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LobstersStory:
    """Lobsters story data model."""

    rank: int
    short_id: str
    title: str
    url: str
    created_at: datetime
    score: int
    upvotes: int
    downvotes: int
    comment_count: int
    description: str
    submitter_user: str
    user_is_author: bool
    tags: list[str] = field(default_factory=list)
    comments_url: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "short_id": self.short_id,
            "title": self.title,
            "url": self.url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "score": self.score,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "comment_count": self.comment_count,
            "description": self.description,
            "submitter_user": self.submitter_user,
            "user_is_author": self.user_is_author,
            "tags": self.tags,
            "comments_url": self.comments_url,
        }

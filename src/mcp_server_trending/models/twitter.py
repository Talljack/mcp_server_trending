"""Twitter/X data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class Tweet(BaseModel):
    """Tweet data model."""

    rank: int
    id: str
    content: str
    author_username: str
    author_display_name: str
    created_at: datetime | None
    url: str
    replies: int
    retweets: int
    likes: int
    quotes: int = 0
    views: int = 0
    is_retweet: bool = False
    is_quote: bool = False
    hashtags: list[str] = field(default_factory=list)
    mentions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "content": self.content[:500] if self.content else "",
            "author": {
                "username": self.author_username,
                "display_name": self.author_display_name,
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "url": self.url,
            "stats": {
                "replies": self.replies,
                "retweets": self.retweets,
                "likes": self.likes,
                "quotes": self.quotes,
                "views": self.views,
            },
            "is_retweet": self.is_retweet,
            "is_quote": self.is_quote,
            "hashtags": self.hashtags,
            "mentions": self.mentions,
        }


@dataclass
class TwitterUser(BaseModel):
    """Twitter user data model."""

    username: str
    display_name: str
    bio: str
    url: str
    followers: int
    following: int
    tweets_count: int
    joined_date: str = ""
    location: str = ""
    website: str = ""
    verified: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "username": self.username,
            "display_name": self.display_name,
            "bio": self.bio[:500] if self.bio else "",
            "url": self.url,
            "stats": {
                "followers": self.followers,
                "following": self.following,
                "tweets": self.tweets_count,
            },
            "joined_date": self.joined_date,
            "location": self.location,
            "website": self.website,
            "verified": self.verified,
        }


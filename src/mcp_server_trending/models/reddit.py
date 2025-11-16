"""Reddit data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class RedditPost(BaseModel):
    """Reddit post model."""

    rank: int
    id: str
    title: str
    url: str
    permalink: str  # Reddit URL
    author: str
    subreddit: str
    subreddit_url: str
    score: int  # upvotes - downvotes
    upvote_ratio: float  # percentage of upvotes
    num_comments: int
    created_at: datetime
    is_self: bool  # True for text posts
    selftext: str = ""  # Post content for text posts
    selftext_html: str | None = None
    domain: str = ""  # External link domain
    flair: str | None = None  # Post flair
    is_video: bool = False
    thumbnail_url: str | None = None
    awards: list[str] = field(default_factory=list)
    distinguished: str | None = None  # "moderator" or "admin" or None
    stickied: bool = False
    over_18: bool = False  # NSFW flag


@dataclass
class SubredditInfo(BaseModel):
    """Subreddit information model."""

    name: str
    display_name: str
    url: str
    description: str
    subscribers: int
    active_users: int
    created_at: datetime
    is_nsfw: bool = False
    public_description: str = ""

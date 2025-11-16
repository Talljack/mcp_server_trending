"""Product Hunt data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class ProductHuntMaker(BaseModel):
    """Product Hunt maker/creator."""

    name: str
    username: str
    url: str
    avatar: str | None = None


@dataclass
class ProductHuntProduct(BaseModel):
    """Product Hunt product."""

    rank: int
    name: str
    tagline: str
    url: str
    product_url: str
    votes: int
    comments_count: int
    thumbnail: str | None = None
    topics: list[str] = field(default_factory=list)
    makers: list[ProductHuntMaker] = field(default_factory=list)
    featured_at: datetime | None = None


@dataclass
class ProductHuntParams:
    """Parameters for Product Hunt queries."""

    time_range: str = "today"  # today, week, month
    topic: str | None = None  # Filter by topic

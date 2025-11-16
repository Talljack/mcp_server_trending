"""Product Hunt data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .base import BaseModel


@dataclass
class ProductHuntMaker(BaseModel):
    """Product Hunt maker/creator."""

    name: str
    username: str
    url: str
    avatar: Optional[str] = None


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
    thumbnail: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    makers: List[ProductHuntMaker] = field(default_factory=list)
    featured_at: Optional[datetime] = None


@dataclass
class ProductHuntParams:
    """Parameters for Product Hunt queries."""

    time_range: str = "today"  # today, week, month
    topic: Optional[str] = None  # Filter by topic

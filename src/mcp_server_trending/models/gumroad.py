"""Gumroad data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class GumroadProduct(BaseModel):
    """Gumroad product data model."""

    rank: int
    id: str
    name: str
    description: str
    url: str
    price: str  # e.g., "$19", "Free", "$0+"
    price_cents: int  # price in cents for sorting
    creator_name: str
    creator_url: str
    thumbnail_url: str
    rating: float  # 0-5 stars
    ratings_count: int
    sales_count: int  # estimated sales if available
    category: str
    tags: list[str] = field(default_factory=list)
    is_featured: bool = False
    currency: str = "USD"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "name": self.name,
            "description": self.description[:500] if self.description else "",
            "url": self.url,
            "price": self.price,
            "price_cents": self.price_cents,
            "creator": {
                "name": self.creator_name,
                "url": self.creator_url,
            },
            "thumbnail_url": self.thumbnail_url,
            "rating": self.rating,
            "ratings_count": self.ratings_count,
            "sales_count": self.sales_count,
            "category": self.category,
            "tags": self.tags,
            "is_featured": self.is_featured,
            "currency": self.currency,
        }


@dataclass
class GumroadCreator(BaseModel):
    """Gumroad creator data model."""

    rank: int
    id: str
    name: str
    bio: str
    url: str
    avatar_url: str
    products_count: int
    followers_count: int
    total_sales: int  # estimated if available
    featured_product: str = ""
    twitter_handle: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "name": self.name,
            "bio": self.bio[:300] if self.bio else "",
            "url": self.url,
            "avatar_url": self.avatar_url,
            "products_count": self.products_count,
            "followers_count": self.followers_count,
            "total_sales": self.total_sales,
            "featured_product": self.featured_product,
            "twitter_handle": self.twitter_handle,
        }


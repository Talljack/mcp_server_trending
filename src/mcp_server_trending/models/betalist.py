"""Betalist data models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BetalistStartup:
    """Betalist startup data model."""

    rank: int
    id: str
    name: str
    tagline: str
    description: str
    url: str
    website_url: str
    upvotes: int
    featured_at: datetime | None = None
    tags: list[str] = field(default_factory=list)
    maker: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "name": self.name,
            "tagline": self.tagline,
            "description": self.description[:500] if self.description else "",
            "url": self.url,
            "website_url": self.website_url,
            "upvotes": self.upvotes,
            "featured_at": self.featured_at.isoformat() if self.featured_at else None,
            "tags": self.tags,
            "maker": self.maker,
        }


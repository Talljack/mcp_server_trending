"""AI Tools Directory data models."""

from dataclasses import dataclass, field

from .base import BaseModel


@dataclass
class AITool(BaseModel):
    """AI Tool from directory."""

    rank: int
    name: str
    description: str
    url: str
    website: str | None = None
    category: str | None = None
    tags: list[str] = field(default_factory=list)
    pricing: str | None = None  # Free, Freemium, Paid, etc.
    rating: float | None = None
    reviews_count: int = 0
    thumbnail: str | None = None
    is_featured: bool = False

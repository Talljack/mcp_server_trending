"""We Work Remotely data models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WeWorkRemotelyJob:
    """We Work Remotely job listing data model."""

    rank: int
    id: str
    title: str
    company: str
    url: str
    published_at: datetime
    category: str
    region: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "url": self.url,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "category": self.category,
            "region": self.region,
            "description": self.description,
            "tags": self.tags,
        }

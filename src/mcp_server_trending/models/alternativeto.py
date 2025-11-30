"""AlternativeTo data models."""

from dataclasses import dataclass, field


@dataclass
class AlternativeToApp:
    """AlternativeTo app/software data model."""

    rank: int
    id: str
    name: str
    description: str
    url: str
    likes: int
    platforms: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    is_free: bool = False
    is_open_source: bool = False
    website_url: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "name": self.name,
            "description": self.description[:500] if self.description else "",
            "url": self.url,
            "likes": self.likes,
            "platforms": self.platforms,
            "tags": self.tags,
            "is_free": self.is_free,
            "is_open_source": self.is_open_source,
            "website_url": self.website_url,
        }


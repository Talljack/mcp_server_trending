"""Papers with Code data models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PapersWithCodePaper:
    """Papers with Code paper data model."""

    rank: int
    id: str
    title: str
    abstract: str
    url_abs: str  # Paper abstract URL
    url_pdf: str  # Paper PDF URL
    arxiv_id: str
    published: datetime | None
    authors: list[str] = field(default_factory=list)
    tasks: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    repository_url: str = ""
    stars: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "title": self.title,
            "abstract": self.abstract[:500] if self.abstract else "",
            "url_abs": self.url_abs,
            "url_pdf": self.url_pdf,
            "arxiv_id": self.arxiv_id,
            "published": self.published.isoformat() if self.published else None,
            "authors": self.authors,
            "tasks": self.tasks,
            "methods": self.methods,
            "repository_url": self.repository_url,
            "stars": self.stars,
        }


@dataclass
class PapersWithCodeMethod:
    """Papers with Code method/model data model."""

    rank: int
    id: str
    name: str
    full_name: str
    description: str
    paper_url: str
    code_url: str
    introduced_year: int | None = None
    num_papers: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description[:500] if self.description else "",
            "paper_url": self.paper_url,
            "code_url": self.code_url,
            "introduced_year": self.introduced_year,
            "num_papers": self.num_papers,
        }


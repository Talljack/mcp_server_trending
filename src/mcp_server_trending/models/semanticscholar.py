"""Semantic Scholar data models."""

from dataclasses import dataclass, field

from .base import BaseModel


@dataclass
class SemanticScholarAuthor(BaseModel):
    """Semantic Scholar author information."""

    author_id: str | None = None
    name: str = ""


@dataclass
class SemanticScholarPaper(BaseModel):
    """Semantic Scholar research paper."""

    rank: int
    paper_id: str
    title: str
    abstract: str | None
    authors: list[SemanticScholarAuthor]
    year: int | None
    citation_count: int
    influential_citation_count: int
    venue: str | None
    publication_date: str | None
    url: str
    is_open_access: bool = False
    open_access_pdf: str | None = None
    fields_of_study: list[str] = field(default_factory=list)


@dataclass
class SemanticScholarQuery:
    """Parameters for Semantic Scholar queries."""

    query: str | None = None  # Search query
    fields_of_study: list[str] | None = None  # e.g., ['Computer Science', 'Medicine']
    year: str | None = None  # Year range like "2020-2023"
    venue: str | None = None  # Conference/journal name
    min_citation_count: int | None = None  # Minimum citations
    open_access_pdf: bool = False  # Only papers with open access PDFs
    sort: str = "citationCount"  # Sort by: citationCount, publicationDate, relevance
    limit: int = 100

"""Data models for cross-platform search and summary."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


@dataclass
class SearchResultItem:
    """A single search result item from any platform."""

    platform: str
    title: str
    url: str
    description: str | None = None
    score: float = 0.0  # Relevance/popularity score
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "platform": self.platform,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "score": self.score,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CrossPlatformSearchResult(BaseModel):
    """Model for cross-platform search results."""

    query: str = Field(..., description="Search query")
    total_results: int = Field(default=0, description="Total number of results")
    platforms_searched: list[str] = Field(
        default_factory=list, description="Platforms that were searched"
    )
    results_by_platform: dict[str, int] = Field(
        default_factory=dict, description="Result count per platform"
    )
    top_results: list[dict] = Field(
        default_factory=list, description="Top results across all platforms"
    )
    search_time_ms: float = Field(default=0.0, description="Search time in milliseconds")
    summary: str = Field(default="", description="Search summary")


class PlatformSummaryItem(BaseModel):
    """Summary of trending items from a single platform."""

    platform: str = Field(..., description="Platform name")
    platform_display_name: str = Field(..., description="Display name for the platform")
    item_count: int = Field(default=0, description="Number of items")
    top_items: list[dict] = Field(default_factory=list, description="Top items from this platform")
    highlights: list[str] = Field(default_factory=list, description="Key highlights")
    fetch_success: bool = Field(default=True, description="Whether fetch was successful")
    error_message: str | None = Field(default=None, description="Error message if fetch failed")


class TrendingSummary(BaseModel):
    """Model for today's trending summary across all platforms."""

    generated_at: str = Field(..., description="When the summary was generated")
    total_platforms: int = Field(default=0, description="Number of platforms included")
    total_items: int = Field(default=0, description="Total trending items across all platforms")
    platform_summaries: list[PlatformSummaryItem] = Field(
        default_factory=list, description="Summary from each platform"
    )
    top_highlights: list[str] = Field(
        default_factory=list, description="Top highlights across all platforms"
    )
    categories: dict[str, int] = Field(
        default_factory=dict, description="Item count by category"
    )
    summary_text: str = Field(default="", description="Human-readable summary")


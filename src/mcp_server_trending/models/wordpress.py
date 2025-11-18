"""Data models for WordPress plugins."""

from pydantic import BaseModel, Field


class WordPressPlugin(BaseModel):
    """Model for a WordPress plugin."""

    rank: int = Field(..., description="Ranking position")
    slug: str = Field(..., description="Plugin slug")
    name: str = Field(..., description="Plugin name")
    version: str = Field(default="", description="Latest version")
    author: str = Field(default="", description="Plugin author")
    author_profile: str | None = Field(default=None, description="Author profile URL")
    description: str = Field(default="", description="Short description")
    short_description: str = Field(default="", description="Very short description")
    rating: float = Field(default=0.0, description="Average rating (0-100)")
    num_ratings: int = Field(default=0, description="Number of ratings")
    active_installs: int = Field(default=0, description="Number of active installations")
    active_installs_display: str = Field(default="", description="Display text for installs")
    downloaded: int = Field(default=0, description="Total downloads")
    last_updated: str = Field(default="", description="Last update date")
    added: str = Field(default="", description="Date added to repository")
    homepage: str | None = Field(default=None, description="Plugin homepage")
    download_link: str | None = Field(default=None, description="Download link")
    url: str = Field(..., description="WordPress.org plugin page URL")
    tags: list[str] = Field(default_factory=list, description="Plugin tags")
    requires_wp: str | None = Field(default=None, description="Required WordPress version")
    requires_php: str | None = Field(default=None, description="Required PHP version")
    tested_up_to: str | None = Field(default=None, description="Tested up to WordPress version")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "slug": "akismet",
                "name": "Akismet Anti-Spam",
                "version": "5.3",
                "author": "Automattic",
                "author_profile": "https://profiles.wordpress.org/automattic/",
                "description": "The best anti-spam protection for your WordPress site.",
                "short_description": "Protect your WordPress site from spam.",
                "rating": 92.5,
                "num_ratings": 5000,
                "active_installs": 5000000,
                "active_installs_display": "5+ million",
                "downloaded": 100000000,
                "last_updated": "2025-11-01",
                "added": "2005-10-01",
                "homepage": "https://akismet.com/",
                "download_link": "https://downloads.wordpress.org/plugin/akismet.zip",
                "url": "https://wordpress.org/plugins/akismet/",
                "tags": ["spam", "comments", "antispam"],
                "requires_wp": "5.8",
                "requires_php": "5.6.20",
                "tested_up_to": "6.4",
            }
        }

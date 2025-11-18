"""Data models for npm packages."""

from pydantic import BaseModel, Field


class NPMPackage(BaseModel):
    """Model for an npm package."""

    rank: int = Field(..., description="Ranking position")
    name: str = Field(..., description="Package name")
    version: str = Field(default="", description="Latest version")
    description: str = Field(default="", description="Package description")
    author: str | None = Field(default=None, description="Package author")
    keywords: list[str] = Field(default_factory=list, description="Package keywords")
    url: str = Field(..., description="npm package URL")
    repository: str | None = Field(default=None, description="Repository URL")
    homepage: str | None = Field(default=None, description="Homepage URL")
    downloads_weekly: int = Field(default=0, description="Weekly downloads")
    downloads_monthly: int = Field(default=0, description="Monthly downloads")
    quality: float = Field(default=0.0, description="Quality score (0-1)")
    popularity: float = Field(default=0.0, description="Popularity score (0-1)")
    maintenance: float = Field(default=0.0, description="Maintenance score (0-1)")
    final_score: float = Field(default=0.0, description="Final score (0-1)")
    last_published: str = Field(default="", description="Last publish date")
    license: str | None = Field(default=None, description="License type")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "name": "react",
                "version": "18.2.0",
                "description": "React is a JavaScript library for building user interfaces.",
                "author": "Meta",
                "keywords": ["react", "framework", "ui"],
                "url": "https://www.npmjs.com/package/react",
                "repository": "https://github.com/facebook/react",
                "homepage": "https://react.dev",
                "downloads_weekly": 20000000,
                "downloads_monthly": 80000000,
                "quality": 0.95,
                "popularity": 0.98,
                "maintenance": 0.99,
                "final_score": 0.97,
                "last_published": "2023-06-15T00:00:00Z",
                "license": "MIT",
            }
        }

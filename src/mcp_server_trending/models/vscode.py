"""Data models for VS Code Marketplace."""

from pydantic import BaseModel, Field


class VSCodeExtension(BaseModel):
    """Model for a VS Code extension."""

    rank: int = Field(..., description="Ranking position")
    extension_id: str = Field(..., description="Extension ID")
    extension_name: str = Field(..., description="Extension display name")
    publisher_id: str = Field(..., description="Publisher ID")
    publisher_name: str = Field(..., description="Publisher display name")
    short_description: str = Field(default="", description="Short description")
    version: str = Field(default="", description="Latest version")
    install_count: int = Field(default=0, description="Number of installs")
    rating: float = Field(default=0.0, description="Average rating (0-5)")
    rating_count: int = Field(default=0, description="Number of ratings")
    url: str = Field(..., description="Marketplace URL")
    repository: str | None = Field(default=None, description="Repository URL if available")
    categories: list[str] = Field(default_factory=list, description="Extension categories")
    tags: list[str] = Field(default_factory=list, description="Extension tags")
    last_updated: str = Field(default="", description="Last update date")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "extension_id": "ms-python.python",
                "extension_name": "Python",
                "publisher_id": "ms-python",
                "publisher_name": "Microsoft",
                "short_description": "IntelliSense, Linting, Debugging, Jupyter",
                "version": "2024.0.0",
                "install_count": 100000000,
                "rating": 4.5,
                "rating_count": 2000,
                "url": "https://marketplace.visualstudio.com/items?itemName=ms-python.python",
                "repository": "https://github.com/microsoft/vscode-python",
                "categories": ["Programming Languages", "Linters"],
                "tags": ["python", "jupyter"],
                "last_updated": "2025-11-17T00:00:00Z",
            }
        }

"""Data models for Chrome Web Store extensions."""

from pydantic import BaseModel, Field


class ChromeExtension(BaseModel):
    """Model for a Chrome extension."""

    rank: int = Field(..., description="Ranking position")
    extension_id: str = Field(..., description="Extension ID")
    name: str = Field(..., description="Extension name")
    short_description: str = Field(default="", description="Short description")
    rating: float = Field(default=0.0, description="Average rating (0-5)")
    rating_count: int = Field(default=0, description="Number of ratings")
    user_count: int = Field(default=0, description="Number of users")
    user_count_display: str = Field(default="", description="Display text for user count")
    category: str = Field(default="", description="Extension category")
    url: str = Field(..., description="Chrome Web Store URL")
    icon_url: str | None = Field(default=None, description="Icon URL")
    developer: str | None = Field(default=None, description="Developer/Publisher name")
    featured: bool = Field(default=False, description="Whether the extension is featured")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "extension_id": "nngceckbapebfimnlniiiahkandclblb",
                "name": "Bitwarden Password Manager",
                "short_description": "A secure and free password manager for all of your devices",
                "rating": 4.7,
                "rating_count": 12000,
                "user_count": 1000000,
                "user_count_display": "1,000,000+ users",
                "category": "Productivity",
                "url": "https://chrome.google.com/webstore/detail/nngceckbapebfimnlniiiahkandclblb",
                "icon_url": "https://example.com/icon.png",
                "developer": "Bitwarden Inc.",
                "featured": True,
            }
        }

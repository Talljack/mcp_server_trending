"""Data models for PyPI packages."""

from pydantic import BaseModel, Field


class PyPIPackage(BaseModel):
    """Model for a PyPI package."""

    rank: int = Field(..., description="Ranking position")
    name: str = Field(..., description="Package name")
    version: str | None = Field(default=None, description="Latest version")
    summary: str = Field(default="", description="Package summary")
    author: str | None = Field(default=None, description="Package author")
    license: str | None = Field(default=None, description="License")
    url: str = Field(..., description="PyPI package URL")
    project_url: str | None = Field(default=None, description="Project/repository URL")
    downloads_last_month: int = Field(default=0, description="Downloads in last month")
    downloads_last_week: int = Field(default=0, description="Downloads in last week")
    downloads_last_day: int = Field(default=0, description="Downloads in last day")
    classifiers: list[str] = Field(default_factory=list, description="Package classifiers")
    keywords: list[str] = Field(default_factory=list, description="Package keywords")
    requires_python: str | None = Field(default=None, description="Required Python version")
    upload_time: str | None = Field(default=None, description="Last upload time")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "name": "requests",
                "version": "2.31.0",
                "summary": "Python HTTP for Humans.",
                "author": "Kenneth Reitz",
                "license": "Apache 2.0",
                "url": "https://pypi.org/project/requests/",
                "project_url": "https://github.com/psf/requests",
                "downloads_last_month": 150000000,
                "downloads_last_week": 35000000,
                "downloads_last_day": 5000000,
                "classifiers": ["Development Status :: 5 - Production/Stable"],
                "keywords": ["http", "requests"],
                "requires_python": ">=3.7",
                "upload_time": "2023-05-22T16:49:48",
            }
        }

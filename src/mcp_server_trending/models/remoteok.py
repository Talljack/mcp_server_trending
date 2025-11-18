"""Data models for RemoteOK jobs."""

from pydantic import BaseModel, Field


class RemoteJob(BaseModel):
    """Model for a remote job."""

    rank: int = Field(..., description="Ranking position")
    id: str = Field(..., description="Job ID")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    company_logo: str | None = Field(default=None, description="Company logo URL")
    description: str = Field(default="", description="Job description")
    location: str = Field(default="Anywhere", description="Job location")
    tags: list[str] = Field(default_factory=list, description="Job tags/skills")
    salary_min: int | None = Field(default=None, description="Minimum salary (USD)")
    salary_max: int | None = Field(default=None, description="Maximum salary (USD)")
    salary_display: str | None = Field(default=None, description="Salary display text")
    url: str = Field(..., description="Job URL")
    apply_url: str | None = Field(default=None, description="Direct apply URL")
    posted_date: str | None = Field(default=None, description="Posted date")
    is_featured: bool = Field(default=False, description="Whether the job is featured")
    job_type: str = Field(default="full-time", description="Job type (full-time, contract, etc.)")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "rank": 1,
                "id": "123456",
                "title": "Senior Python Developer",
                "company": "Acme Corp",
                "company_logo": "https://example.com/logo.png",
                "description": "We are looking for a senior Python developer...",
                "location": "Anywhere",
                "tags": ["python", "django", "aws", "remote"],
                "salary_min": 100000,
                "salary_max": 150000,
                "salary_display": "$100k - $150k",
                "url": "https://remoteok.com/remote-jobs/123456",
                "apply_url": "https://apply.example.com/job/123456",
                "posted_date": "2025-11-17",
                "is_featured": False,
                "job_type": "full-time",
            }
        }

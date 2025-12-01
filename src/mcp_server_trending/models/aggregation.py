"""Data models for aggregation analysis."""

from pydantic import BaseModel, Field


class TechStackAnalysis(BaseModel):
    """Model for tech stack analysis across platforms."""

    tech_name: str = Field(..., description="Technology name")
    github_repos: int = Field(default=0, description="Number of trending GitHub repos")
    npm_packages: int = Field(default=0, description="Number of related npm packages")
    pypi_packages: int = Field(default=0, description="Number of related PyPI packages")
    stackoverflow_questions: int = Field(default=0, description="Stack Overflow question count")
    vscode_extensions: int = Field(default=0, description="Number of VS Code extensions")
    job_postings: int = Field(default=0, description="Number of job postings")
    total_score: float = Field(default=0.0, description="Aggregated popularity score")
    summary: str = Field(default="", description="Analysis summary")


class IndieRevenueDashboard(BaseModel):
    """Model for indie revenue dashboard."""

    total_projects: int = Field(
        default=0, description="Total number of revenue-generating projects"
    )
    average_mrr: float = Field(default=0.0, description="Average MRR across projects")
    top_categories: list[str] = Field(default_factory=list, description="Top revenue categories")
    success_stories_count: int = Field(
        default=0, description="Number of success stories (>$10k MRR)"
    )
    data_sources: list[str] = Field(default_factory=list, description="Data sources used")
    summary: str = Field(default="", description="Dashboard summary")


class TopicTrends(BaseModel):
    """Model for topic trends across platforms."""

    topic: str = Field(..., description="Topic name")
    hackernews_mentions: int = Field(default=0, description="HackerNews story count")
    github_repos: int = Field(default=0, description="Related GitHub repos")
    stackoverflow_tags: int = Field(default=0, description="Stack Overflow tag count")
    dev_articles: int = Field(default=0, description="dev.to article count")
    juejin_articles: int = Field(default=0, description="Juejin article count")
    total_mentions: int = Field(default=0, description="Total mentions across platforms")
    trending_score: float = Field(default=0.0, description="Trending score")
    summary: str = Field(default="", description="Trend analysis summary")

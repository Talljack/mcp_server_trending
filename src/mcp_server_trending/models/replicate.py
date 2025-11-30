"""Replicate data models."""

from dataclasses import dataclass


@dataclass
class ReplicateModel:
    """Replicate AI model data model."""

    rank: int
    owner: str
    name: str
    description: str
    url: str
    run_count: int
    github_url: str = ""
    paper_url: str = ""
    license: str = ""
    visibility: str = "public"
    latest_version: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "owner": self.owner,
            "name": self.name,
            "full_name": f"{self.owner}/{self.name}",
            "description": self.description[:500] if self.description else "",
            "url": self.url,
            "run_count": self.run_count,
            "github_url": self.github_url,
            "paper_url": self.paper_url,
            "license": self.license,
            "visibility": self.visibility,
            "latest_version": self.latest_version,
        }


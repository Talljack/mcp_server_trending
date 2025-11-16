"""TrustMRR data models."""

from dataclasses import dataclass
from datetime import datetime

from .base import BaseModel


@dataclass
class TrustMRRProject(BaseModel):
    """TrustMRR project with revenue data."""

    rank: int
    name: str
    description: str
    url: str
    mrr: float  # Monthly Recurring Revenue in USD
    mrr_growth: float | None = None  # MRR growth percentage
    arr: float | None = None  # Annual Recurring Revenue
    founded_at: datetime | None = None
    category: str | None = None
    founders: list[str] | None = None
    twitter_url: str | None = None
    is_verified: bool = False

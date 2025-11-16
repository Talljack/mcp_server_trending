"""Models package."""

from .base import BaseModel, TrendingResponse
from .github import GitHubDeveloper, GitHubRepository, GitHubTrendingParams
from .hackernews import HackerNewsParams, HackerNewsStory
from .producthunt import ProductHuntMaker, ProductHuntParams, ProductHuntProduct

__all__ = [
    "BaseModel",
    "TrendingResponse",
    "GitHubDeveloper",
    "GitHubRepository",
    "GitHubTrendingParams",
    "ProductHuntProduct",
    "ProductHuntMaker",
    "ProductHuntParams",
    "HackerNewsStory",
    "HackerNewsParams",
]

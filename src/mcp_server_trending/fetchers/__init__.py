"""Fetchers package."""

from .base import BaseFetcher
from .github import GitHubTrendingFetcher
from .hackernews import HackerNewsFetcher
from .producthunt import ProductHuntFetcher

__all__ = [
    "BaseFetcher",
    "GitHubTrendingFetcher",
    "HackerNewsFetcher",
    "ProductHuntFetcher",
]

"""Fetchers package."""

from .base import BaseFetcher
from .github import GitHubTrendingFetcher
from .hackernews import HackerNewsFetcher
from .producthunt import ProductHuntFetcher
from .indiehackers import IndieHackersFetcher
from .reddit import RedditFetcher
from .openrouter import OpenRouterFetcher

__all__ = [
    "BaseFetcher",
    "GitHubTrendingFetcher",
    "HackerNewsFetcher",
    "ProductHuntFetcher",
    "IndieHackersFetcher",
    "RedditFetcher",
    "OpenRouterFetcher",
]

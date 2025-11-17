"""Fetchers package."""

from .base import BaseFetcher
from .github import GitHubTrendingFetcher
from .hackernews import HackerNewsFetcher
from .producthunt import ProductHuntFetcher
from .indiehackers import IndieHackersFetcher
from .reddit import RedditFetcher
from .openrouter import OpenRouterFetcher
from .trustmrr import TrustMRRFetcher
from .aitools import AIToolsFetcher
from .huggingface import HuggingFaceFetcher
from .v2ex import V2EXFetcher
from .juejin import JuejinFetcher
from .devto import DevToFetcher
from .modelscope import ModelScopeFetcher
from .stackoverflow import StackOverflowFetcher
from .awesome import AwesomeFetcher

__all__ = [
    "BaseFetcher",
    "GitHubTrendingFetcher",
    "HackerNewsFetcher",
    "ProductHuntFetcher",
    "IndieHackersFetcher",
    "RedditFetcher",
    "OpenRouterFetcher",
    "TrustMRRFetcher",
    "AIToolsFetcher",
    "HuggingFaceFetcher",
    "V2EXFetcher",
    "JuejinFetcher",
    "DevToFetcher",
    "ModelScopeFetcher",
    "StackOverflowFetcher",
    "AwesomeFetcher",
]

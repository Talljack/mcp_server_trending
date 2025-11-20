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
from .vscode import VSCodeMarketplaceFetcher
from .npm import NPMFetcher
from .chrome import ChromeWebStoreFetcher
from .pypi import PyPIFetcher
from .remoteok import RemoteOKFetcher
from .wordpress import WordPressFetcher
from .aggregation import AggregationFetcher
from .arxiv import ArxivFetcher
from .semanticscholar import SemanticScholarFetcher
from .openreview import OpenReviewFetcher
from .hashnode import HashnodeFetcher
from .codepen import CodePenFetcher
from .medium import MediumFetcher

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
    "VSCodeMarketplaceFetcher",
    "NPMFetcher",
    "ChromeWebStoreFetcher",
    "PyPIFetcher",
    "RemoteOKFetcher",
    "WordPressFetcher",
    "AggregationFetcher",
    "ArxivFetcher",
    "SemanticScholarFetcher",
    "OpenReviewFetcher",
    "HashnodeFetcher",
    "CodePenFetcher",
    "MediumFetcher",
]

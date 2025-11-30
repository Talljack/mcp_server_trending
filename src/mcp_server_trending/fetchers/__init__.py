"""Fetchers package."""

from .aggregation import AggregationFetcher
from .aitools import AIToolsFetcher
from .alternativeto import AlternativeToFetcher
from .arxiv import ArxivFetcher
from .awesome import AwesomeFetcher
from .base import BaseFetcher
from .betalist import BetalistFetcher
from .chrome import ChromeWebStoreFetcher
from .codepen import CodePenFetcher
from .devto import DevToFetcher
from .echojs import EchoJSFetcher
from .github import GitHubTrendingFetcher
from .hackernews import HackerNewsFetcher
from .hashnode import HashnodeFetcher
from .huggingface import HuggingFaceFetcher
from .indiehackers import IndieHackersFetcher
from .juejin import JuejinFetcher
from .lobsters import LobstersFetcher
from .medium import MediumFetcher
from .modelscope import ModelScopeFetcher
from .npm import NPMFetcher
from .openreview import OpenReviewFetcher
from .openrouter import OpenRouterFetcher
from .paperswithcode import PapersWithCodeFetcher
from .producthunt import ProductHuntFetcher
from .pypi import PyPIFetcher
from .reddit import RedditFetcher
from .remoteok import RemoteOKFetcher
from .replicate import ReplicateFetcher
from .semanticscholar import SemanticScholarFetcher
from .stackoverflow import StackOverflowFetcher
from .trustmrr import TrustMRRFetcher
from .v2ex import V2EXFetcher
from .vscode import VSCodeMarketplaceFetcher
from .weworkremotely import WeWorkRemotelyFetcher
from .wordpress import WordPressFetcher

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
    "LobstersFetcher",
    "EchoJSFetcher",
    "WeWorkRemotelyFetcher",
    "PapersWithCodeFetcher",
    "AlternativeToFetcher",
    "ReplicateFetcher",
    "BetalistFetcher",
]

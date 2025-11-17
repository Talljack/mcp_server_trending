"""Models package."""

from .base import BaseModel, TrendingResponse
from .github import GitHubDeveloper, GitHubRepository, GitHubTrendingParams
from .hackernews import HackerNewsParams, HackerNewsStory
from .producthunt import ProductHuntMaker, ProductHuntParams, ProductHuntProduct
from .indiehackers import IndieHackersPost, IncomeReport, ProjectMilestone
from .reddit import RedditPost, SubredditInfo
from .openrouter import LLMModel, ModelComparison, ModelRanking
from .trustmrr import TrustMRRProject
from .aitools import AITool
from .huggingface import HFModel, HFDataset
from .v2ex import V2EXTopic
from .juejin import JuejinArticle
from .devto import DevToArticle
from .modelscope import ModelScopeModel, ModelScopeDataset
from .stackoverflow import StackOverflowTag, StackOverflowParams
from .awesome import AwesomeList, AwesomeParams

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
    "IndieHackersPost",
    "IncomeReport",
    "ProjectMilestone",
    "RedditPost",
    "SubredditInfo",
    "LLMModel",
    "ModelComparison",
    "ModelRanking",
    "TrustMRRProject",
    "AITool",
    "HFModel",
    "HFDataset",
    "V2EXTopic",
    "JuejinArticle",
    "DevToArticle",
    "ModelScopeModel",
    "ModelScopeDataset",
    "StackOverflowTag",
    "StackOverflowParams",
    "AwesomeList",
    "AwesomeParams",
]

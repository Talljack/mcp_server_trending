"""Models package."""

from .aitools import AITool
from .alternativeto import AlternativeToApp
from .arxiv import ArxivPaper, ArxivQuery
from .awesome import AwesomeList, AwesomeParams
from .base import BaseModel, TrendingResponse
from .betalist import BetalistStartup
from .codepen import CodePenPen, CodePenUser
from .devto import DevToArticle
from .echojs import EchoJSNews
from .github import GitHubDeveloper, GitHubRepository, GitHubTrendingParams
from .hackernews import HackerNewsParams, HackerNewsStory
from .hashnode import HashnodeArticle, HashnodeAuthor
from .huggingface import HFDataset, HFModel
from .indiehackers import IncomeReport, IndieHackersPost, ProjectMilestone
from .juejin import JuejinArticle
from .lobsters import LobstersStory
from .medium import MediumArticle, MediumAuthor
from .modelscope import ModelScopeDataset, ModelScopeModel
from .openreview import OpenReviewPaper, OpenReviewQuery
from .openrouter import LLMModel, ModelComparison, ModelRanking
from .paperswithcode import PapersWithCodeMethod, PapersWithCodePaper
from .producthunt import ProductHuntMaker, ProductHuntParams, ProductHuntProduct
from .reddit import RedditPost, SubredditInfo
from .replicate import ReplicateModel
from .semanticscholar import (
    SemanticScholarAuthor,
    SemanticScholarPaper,
    SemanticScholarQuery,
)
from .stackoverflow import StackOverflowParams, StackOverflowTag
from .trustmrr import TrustMRRProject
from .twitter import Tweet, TwitterUser
from .v2ex import V2EXTopic
from .weworkremotely import WeWorkRemotelyJob

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
    "ArxivPaper",
    "ArxivQuery",
    "SemanticScholarAuthor",
    "SemanticScholarPaper",
    "SemanticScholarQuery",
    "OpenReviewPaper",
    "OpenReviewQuery",
    "HashnodeArticle",
    "HashnodeAuthor",
    "CodePenPen",
    "CodePenUser",
    "MediumArticle",
    "MediumAuthor",
    "LobstersStory",
    "EchoJSNews",
    "WeWorkRemotelyJob",
    "PapersWithCodePaper",
    "PapersWithCodeMethod",
    "AlternativeToApp",
    "ReplicateModel",
    "BetalistStartup",
    "Tweet",
    "TwitterUser",
]

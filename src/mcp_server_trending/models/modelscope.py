"""ModelScope (魔塔社区) data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class ModelScopeModel(BaseModel):
    """ModelScope model."""

    rank: int
    id: str  # Model ID
    name: str
    namespace: str  # Organization/user namespace
    task: str | None = None  # Task type (e.g., "text-generation")

    # Model info
    description: str | None = None
    chinese_name: str | None = None

    # Metrics
    downloads: int = 0
    likes: int = 0
    stars: int = 0

    # Tags and categories
    tags: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)  # e.g., "pytorch", "tensorflow"

    # URLs
    url: str | None = None

    # Timestamps
    gmt_create: datetime | None = None
    gmt_modified: datetime | None = None


@dataclass
class ModelScopeDataset(BaseModel):
    """ModelScope dataset."""

    rank: int
    id: str  # Dataset ID
    name: str
    namespace: str  # Organization/user namespace

    # Dataset info
    description: str | None = None
    chinese_name: str | None = None

    # Metrics
    downloads: int = 0
    likes: int = 0
    stars: int = 0

    # Tags and categories
    tags: list[str] = field(default_factory=list)
    task_categories: list[str] = field(default_factory=list)

    # URLs
    url: str | None = None

    # Timestamps
    gmt_create: datetime | None = None
    gmt_modified: datetime | None = None

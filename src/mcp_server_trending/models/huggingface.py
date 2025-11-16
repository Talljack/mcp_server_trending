"""HuggingFace data models."""

from dataclasses import dataclass, field
from datetime import datetime

from .base import BaseModel


@dataclass
class HFModel(BaseModel):
    """HuggingFace model."""

    rank: int
    id: str  # e.g., "meta-llama/Llama-2-7b-hf"
    name: str
    author: str | None = None
    downloads: int = 0
    likes: int = 0
    tags: list[str] = field(default_factory=list)
    pipeline_tag: str | None = None  # Task type (e.g., "text-generation")
    library_name: str | None = None  # e.g., "transformers", "diffusers"
    created_at: datetime | None = None
    last_modified: datetime | None = None
    model_url: str | None = None
    description: str | None = None


@dataclass
class HFDataset(BaseModel):
    """HuggingFace dataset."""

    rank: int
    id: str  # e.g., "squad"
    name: str
    author: str | None = None
    downloads: int = 0
    likes: int = 0
    tags: list[str] = field(default_factory=list)
    task_categories: list[str] = field(default_factory=list)
    size_categories: list[str] = field(default_factory=list)
    language: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    last_modified: datetime | None = None
    dataset_url: str | None = None
    description: str | None = None

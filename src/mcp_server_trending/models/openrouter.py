"""OpenRouter LLM models data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .base import BaseModel


@dataclass
class LLMModel(BaseModel):
    """OpenRouter LLM model information."""

    rank: int
    id: str  # Model ID, e.g., "anthropic/claude-3-opus"
    name: str  # Display name
    provider: str  # e.g., "Anthropic", "OpenAI"
    description: str
    context_length: int  # Max context window
    pricing: dict[str, float] = field(
        default_factory=dict
    )  # {"prompt": 0.015, "completion": 0.075}

    # Performance metrics
    performance_score: float | None = None
    latency_ms: int | None = None

    # Capabilities
    supports_vision: bool = False
    supports_function_calling: bool = False
    supports_streaming: bool = True

    # Popularity metrics
    total_requests: int | None = None
    requests_per_day: int | None = None

    # Model metadata
    created_at: datetime | None = None
    architecture: str | None = None  # e.g., "Transformer"
    modality: list[str] = field(default_factory=lambda: ["text"])  # ["text", "image", "code"]

    # URLs
    model_url: str | None = None
    provider_url: str | None = None
    documentation_url: str | None = None


@dataclass
class ModelComparison(BaseModel):
    """Comparison metrics for multiple models."""

    metric_name: str  # e.g., "cost_per_1k_tokens", "performance_score"
    models: list[dict[str, Any]] = field(
        default_factory=list
    )  # [{"model_id": "...", "value": 0.01}]
    best_model_id: str | None = None
    worst_model_id: str | None = None


@dataclass
class ModelRanking(BaseModel):
    """Model ranking by specific criteria."""

    ranking_type: str  # e.g., "most_popular", "best_value", "fastest"
    description: str
    models: list[str] = field(default_factory=list)  # List of model IDs in ranking order
    updated_at: datetime = field(default_factory=datetime.now)

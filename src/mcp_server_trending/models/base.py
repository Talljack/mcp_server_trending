"""Base models for all platform data structures."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BaseModel:
    """Base model for all data structures."""

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, BaseModel):
                result[key] = value.to_dict()
            elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
                result[key] = [item.to_dict() for item in value]
            else:
                result[key] = value
        return result


@dataclass
class TrendingResponse(BaseModel):
    """Standard response format for all trending data."""

    success: bool
    platform: str
    data_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    cache_hit: bool = False
    data: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with proper datetime formatting."""
        result = super().to_dict()
        # Ensure data items are properly serialized
        if self.data:
            serialized_data = []
            for item in self.data:
                if isinstance(item, BaseModel):
                    serialized_data.append(item.to_dict())
                elif hasattr(item, "model_dump"):
                    # Pydantic BaseModel
                    serialized_data.append(item.model_dump())
                else:
                    serialized_data.append(item)
            result["data"] = serialized_data
        return result

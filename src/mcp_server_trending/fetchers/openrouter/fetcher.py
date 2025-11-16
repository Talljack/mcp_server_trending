"""OpenRouter LLM rankings fetcher implementation."""

from typing import Any

from ...config import config
from ...models import LLMModel, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class OpenRouterFetcher(BaseFetcher):
    """Fetcher for OpenRouter LLM model rankings."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://openrouter.ai/api/v1"
        # 从 config 读取 API key
        self.api_key = config.openrouter_api_key

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "openrouter"

    def _check_api_key(self) -> TrendingResponse | None:
        """
        Check if API key is configured.

        Returns:
            None if API key is configured, error response otherwise
        """
        if not self.api_key:
            error_msg = (
                "❌ OpenRouter API key not configured.\n\n"
                "To use OpenRouter tools, you need to configure an API key:\n\n"
                "Option 1: Using .env file (recommended)\n"
                "  1. Copy .env.example to .env\n"
                "  2. Add: OPENROUTER_API_KEY=your_api_key_here\n"
                "  3. Get your key at: https://openrouter.ai/keys\n\n"
                "Option 2: Environment variable\n"
                "  export OPENROUTER_API_KEY=your_api_key_here\n\n"
                "📖 OpenRouter provides free tier with limited usage.\n"
                "🔑 You can get an API key at: https://openrouter.ai/keys"
            )
            logger.error("OpenRouter API key not configured")
            return self._create_response(
                success=False,
                data_type="error",
                data=[],
                error=error_msg,
                metadata={
                    "requires_api_key": True,
                    "api_key_url": "https://openrouter.ai/keys",
                },
            )
        return None

    async def fetch_models(
        self, limit: int | None = None, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch all available LLM models from OpenRouter.

        Args:
            limit: Maximum number of models to return (None for all)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with LLM models
        """
        return await self.fetch_with_cache(
            data_type="models",
            fetch_func=self._fetch_models_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_models_internal(self, limit: int | None = None) -> TrendingResponse:
        """Internal implementation to fetch models."""
        # Check API key
        error_response = self._check_api_key()
        if error_response:
            return error_response

        try:
            url = f"{self.base_url}/models"
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            logger.info("Fetching OpenRouter models list")

            response = await self.http_client.get(url, headers=headers)
            data = response.json()

            models = self._parse_models(data.get("data", []), limit)

            return self._create_response(
                success=True,
                data_type="models",
                data=models,
                metadata={"total_count": len(models), "limit": limit},
            )

        except Exception as e:
            logger.error(f"Error fetching OpenRouter models: {e}")
            return self._create_response(success=False, data_type="models", data=[], error=str(e))

    async def fetch_popular_models(
        self, limit: int = 20, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch most popular LLM models based on usage.

        Args:
            limit: Number of models to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with popular models
        """
        # First fetch all models
        all_models_response = await self.fetch_models(use_cache=use_cache)

        if not all_models_response.success:
            return all_models_response

        # Sort by popularity (requests per day if available)
        models = all_models_response.data
        sorted_models = sorted(
            models,
            key=lambda m: getattr(m, "requests_per_day", 0) or 0,
            reverse=True,
        )[:limit]

        return self._create_response(
            success=True,
            data_type="popular_models",
            data=sorted_models,
            metadata={"ranking_type": "most_popular", "total_count": len(sorted_models)},
        )

    async def fetch_best_value_models(
        self, limit: int = 20, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch best value LLM models (performance vs cost).

        Args:
            limit: Number of models to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with best value models
        """
        all_models_response = await self.fetch_models(use_cache=use_cache)

        if not all_models_response.success:
            return all_models_response

        # Calculate value score (performance / cost)
        valued_models = []
        for model in all_models_response.data:
            if hasattr(model, "pricing") and model.pricing:
                prompt_cost = model.pricing.get("prompt", 0)
                completion_cost = model.pricing.get("completion", 0)
                avg_cost = (
                    (prompt_cost + completion_cost) / 2 if prompt_cost or completion_cost else 0
                )

                performance = getattr(model, "performance_score", 50) or 50

                if avg_cost > 0:
                    value_score = performance / (avg_cost * 1000)  # per 1k tokens
                    model.value_score = value_score
                    valued_models.append(model)

        # Sort by value score
        sorted_models = sorted(
            valued_models, key=lambda m: getattr(m, "value_score", 0), reverse=True
        )[:limit]

        return self._create_response(
            success=True,
            data_type="best_value_models",
            data=sorted_models,
            metadata={"ranking_type": "best_value", "total_count": len(sorted_models)},
        )

    async def fetch_fastest_models(
        self, limit: int = 20, use_cache: bool = True
    ) -> TrendingResponse:
        """
        Fetch fastest LLM models based on latency.

        Args:
            limit: Number of models to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with fastest models
        """
        all_models_response = await self.fetch_models(use_cache=use_cache)

        if not all_models_response.success:
            return all_models_response

        # Filter models with latency data and sort by speed
        models_with_latency = [
            m for m in all_models_response.data if hasattr(m, "latency_ms") and m.latency_ms
        ]

        sorted_models = sorted(models_with_latency, key=lambda m: m.latency_ms or float("inf"))[
            :limit
        ]

        return self._create_response(
            success=True,
            data_type="fastest_models",
            data=sorted_models,
            metadata={"ranking_type": "fastest", "total_count": len(sorted_models)},
        )

    def _parse_models(
        self, models_data: list[dict[str, Any]], limit: int | None = None
    ) -> list[LLMModel]:
        """Parse models from OpenRouter API response."""
        models = []
        rank = 1

        for model_data in models_data:
            try:
                # Parse pricing
                pricing = {}
                if "pricing" in model_data:
                    pricing_data = model_data["pricing"]
                    pricing["prompt"] = float(pricing_data.get("prompt", 0))
                    pricing["completion"] = float(pricing_data.get("completion", 0))

                # Extract provider from model ID
                model_id = model_data.get("id", "")
                provider = model_id.split("/")[0] if "/" in model_id else "Unknown"

                model = LLMModel(
                    rank=rank,
                    id=model_id,
                    name=model_data.get("name", model_id),
                    provider=provider.title(),
                    description=model_data.get("description", ""),
                    context_length=model_data.get("context_length", 0),
                    pricing=pricing,
                    supports_vision="vision" in model_data.get("modality", []),
                    supports_function_calling=model_data.get("supports_function_calling", False),
                    supports_streaming=model_data.get("supports_streaming", True),
                    architecture=model_data.get("architecture"),
                    modality=model_data.get("modality", ["text"]),
                    model_url=f"https://openrouter.ai/models/{model_id}",
                )

                models.append(model)
                rank += 1

                if limit and rank > limit:
                    break

            except Exception as e:
                logger.warning(f"Error parsing OpenRouter model: {e}")
                continue

        return models

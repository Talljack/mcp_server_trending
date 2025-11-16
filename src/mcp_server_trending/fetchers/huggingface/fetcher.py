"""HuggingFace models and datasets fetcher implementation."""

from datetime import datetime
from typing import Any

from ...config import config
from ...models import HFDataset, HFModel, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class HuggingFaceFetcher(BaseFetcher):
    """Fetcher for HuggingFace models and datasets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://huggingface.co/api"
        # 从 config 读取 API token (可选)
        self.api_token = config.huggingface_token

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "huggingface"

    def _check_api_token(self) -> TrendingResponse | None:
        """
        Check if API token is configured.

        Note: HuggingFace API works without token but has rate limits.
        Token is optional but recommended for higher limits.

        Returns:
            None if token is configured or not required, warning response otherwise
        """
        if not self.api_token:
            logger.warning(
                "HuggingFace token not configured. Using public API with rate limits."
            )
        return None

    async def fetch_trending_models(
        self,
        sort_by: str = "downloads",
        task: str | None = None,
        library: str | None = None,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending models from HuggingFace.

        Args:
            sort_by: Sort by 'downloads', 'likes', or 'modified'
            task: Filter by task (e.g., 'text-generation', 'image-classification')
            library: Filter by library (e.g., 'transformers', 'diffusers')
            limit: Maximum number of models to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with HuggingFace models
        """
        cache_key = f"models:sort={sort_by}:task={task}:lib={library}:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_models_internal,
            use_cache=use_cache,
            sort_by=sort_by,
            task=task,
            library=library,
            limit=limit,
        )

    async def _fetch_models_internal(
        self,
        sort_by: str = "downloads",
        task: str | None = None,
        library: str | None = None,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch models."""
        self._check_api_token()

        try:
            url = f"{self.base_url}/models"
            params = {
                "sort": sort_by,
                "direction": "-1",  # Descending
                "limit": limit,
            }

            if task:
                params["filter"] = task
            if library:
                params["library"] = library

            headers = {}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"

            logger.info(f"Fetching HuggingFace models (sort={sort_by}, limit={limit})")

            response = await self.http_client.get(url, params=params, headers=headers)
            data = response.json()

            models = self._parse_models(data, limit)

            return self._create_response(
                success=True,
                data_type="models",
                data=models,
                metadata={
                    "total_count": len(models),
                    "sort_by": sort_by,
                    "task": task,
                    "library": library,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching HuggingFace models: {e}")
            return self._create_response(success=False, data_type="models", data=[], error=str(e))

    async def fetch_trending_datasets(
        self,
        sort_by: str = "downloads",
        task: str | None = None,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending datasets from HuggingFace.

        Args:
            sort_by: Sort by 'downloads', 'likes', or 'modified'
            task: Filter by task category
            limit: Maximum number of datasets to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with HuggingFace datasets
        """
        cache_key = f"datasets:sort={sort_by}:task={task}:limit={limit}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_datasets_internal,
            use_cache=use_cache,
            sort_by=sort_by,
            task=task,
            limit=limit,
        )

    async def _fetch_datasets_internal(
        self,
        sort_by: str = "downloads",
        task: str | None = None,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch datasets."""
        self._check_api_token()

        try:
            url = f"{self.base_url}/datasets"
            params = {
                "sort": sort_by,
                "direction": "-1",  # Descending
                "limit": limit,
            }

            if task:
                params["filter"] = task

            headers = {}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"

            logger.info(f"Fetching HuggingFace datasets (sort={sort_by}, limit={limit})")

            response = await self.http_client.get(url, params=params, headers=headers)
            data = response.json()

            datasets = self._parse_datasets(data, limit)

            return self._create_response(
                success=True,
                data_type="datasets",
                data=datasets,
                metadata={
                    "total_count": len(datasets),
                    "sort_by": sort_by,
                    "task": task,
                    "limit": limit,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching HuggingFace datasets: {e}")
            return self._create_response(success=False, data_type="datasets", data=[], error=str(e))

    def _parse_models(
        self, models_data: list[dict[str, Any]], limit: int = 20
    ) -> list[HFModel]:
        """Parse models from HuggingFace API response."""
        models = []
        rank = 1

        for model_data in models_data[:limit]:
            try:
                model_id = model_data.get("id", "")
                author = model_id.split("/")[0] if "/" in model_id else None
                name = model_id.split("/")[-1] if "/" in model_id else model_id

                # Parse dates
                created_at = None
                if "createdAt" in model_data:
                    try:
                        created_at = datetime.fromisoformat(
                            model_data["createdAt"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                last_modified = None
                if "lastModified" in model_data:
                    try:
                        last_modified = datetime.fromisoformat(
                            model_data["lastModified"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                model = HFModel(
                    rank=rank,
                    id=model_id,
                    name=name,
                    author=author,
                    downloads=model_data.get("downloads", 0),
                    likes=model_data.get("likes", 0),
                    tags=model_data.get("tags", []),
                    pipeline_tag=model_data.get("pipeline_tag"),
                    library_name=model_data.get("library_name"),
                    created_at=created_at,
                    last_modified=last_modified,
                    model_url=f"https://huggingface.co/{model_id}",
                    description=model_data.get("description", ""),
                )

                models.append(model)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing HuggingFace model: {e}")
                continue

        return models

    def _parse_datasets(
        self, datasets_data: list[dict[str, Any]], limit: int = 20
    ) -> list[HFDataset]:
        """Parse datasets from HuggingFace API response."""
        datasets = []
        rank = 1

        for dataset_data in datasets_data[:limit]:
            try:
                dataset_id = dataset_data.get("id", "")
                author = dataset_id.split("/")[0] if "/" in dataset_id else None
                name = dataset_id.split("/")[-1] if "/" in dataset_id else dataset_id

                # Parse dates
                created_at = None
                if "createdAt" in dataset_data:
                    try:
                        created_at = datetime.fromisoformat(
                            dataset_data["createdAt"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                last_modified = None
                if "lastModified" in dataset_data:
                    try:
                        last_modified = datetime.fromisoformat(
                            dataset_data["lastModified"].replace("Z", "+00:00")
                        )
                    except (ValueError, AttributeError):
                        pass

                dataset = HFDataset(
                    rank=rank,
                    id=dataset_id,
                    name=name,
                    author=author,
                    downloads=dataset_data.get("downloads", 0),
                    likes=dataset_data.get("likes", 0),
                    tags=dataset_data.get("tags", []),
                    task_categories=dataset_data.get("task_categories", []),
                    size_categories=dataset_data.get("size_categories", []),
                    language=dataset_data.get("language", []),
                    created_at=created_at,
                    last_modified=last_modified,
                    dataset_url=f"https://huggingface.co/datasets/{dataset_id}",
                    description=dataset_data.get("description", ""),
                )

                datasets.append(dataset)
                rank += 1

            except Exception as e:
                logger.warning(f"Error parsing HuggingFace dataset: {e}")
                continue

        return datasets

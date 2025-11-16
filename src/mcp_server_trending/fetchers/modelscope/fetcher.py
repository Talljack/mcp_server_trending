"""ModelScope (魔塔社区) fetcher implementation."""

from datetime import datetime
from typing import Any

from ...models import ModelScopeDataset, ModelScopeModel, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class ModelScopeFetcher(BaseFetcher):
    """Fetcher for ModelScope (魔塔社区) models and datasets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.web_url = "https://modelscope.cn"
        self.api_base_url = "https://modelscope.cn/api/v1/dolphin"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "modelscope"

    async def fetch_models(
        self,
        page_number: int = 1,
        page_size: int = 20,
        sort_by: str = "Default",  # Default, downloads, stars, etc.
        search_text: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch models from ModelScope via API.

        Args:
            page_number: Page number
            page_size: Items per page
            sort_by: Sort by (Default, downloads, stars, etc.)
            search_text: Search text to filter models by name
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with ModelScope models
        """
        cache_key = f"models:page={page_number}:size={page_size}:sort={sort_by}:search={search_text}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_models_internal,
            use_cache=use_cache,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
            search_text=search_text,
        )

    async def _fetch_models_internal(
        self,
        page_number: int = 1,
        page_size: int = 20,
        sort_by: str = "Default",
        search_text: str | None = None,
    ) -> TrendingResponse:
        """Internal implementation to fetch models via API."""
        try:
            url = f"{self.api_base_url}/models"

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Referer": "https://modelscope.cn/models",
            }

            # Build request payload according to API structure
            payload = {
                "PageSize": page_size,
                "PageNumber": page_number,
                "SortBy": sort_by,
                "Target": "",
                "SingleCriterion": [],
                "Criterion": [],
            }

            if search_text:
                payload["Name"] = search_text
            else:
                payload["Name"] = ""

            logger.info(
                f"Fetching ModelScope models via API (page={page_number}, size={page_size}, sort={sort_by}, search={search_text})"
            )

            # Use PUT method as required by the API
            response = await self.http_client.put(url, json=payload, headers=headers)

            if response.status_code != 200:
                logger.warning(f"ModelScope API returned status {response.status_code}")
                return self._create_response(
                    success=False,
                    data_type="models",
                    data=[],
                    error=f"HTTP {response.status_code}",
                )

            data = response.json()

            if data.get("Code") != 200 or not data.get("Success", False):
                error_msg = data.get("Message", "Unknown error")
                logger.warning(f"ModelScope API error: {error_msg}")
                return self._create_response(
                    success=False,
                    data_type="models",
                    data=[],
                    error=error_msg,
                )

            # Parse models from response
            models = self._parse_models(data, page_size)

            total_count = 0
            if "Data" in data and isinstance(data["Data"], dict):
                if "Model" in data["Data"] and isinstance(data["Data"]["Model"], dict):
                    total_count = data["Data"]["Model"].get("TotalCount", len(models))

            return self._create_response(
                success=True,
                data_type="models",
                data=models,
                metadata={
                    "total_count": total_count,
                    "page_number": page_number,
                    "page_size": page_size,
                    "sort_by": sort_by,
                    "search_text": search_text,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching ModelScope models: {e}")
            return self._create_response(success=False, data_type="models", data=[], error=str(e))

    async def fetch_datasets(
        self,
        page_number: int = 1,
        page_size: int = 20,
        target: str = "",
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch datasets from ModelScope via API.

        Args:
            page_number: Page number
            page_size: Items per page
            target: Target filter (optional)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with ModelScope datasets
        """
        cache_key = f"datasets:page={page_number}:size={page_size}:target={target}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_datasets_internal,
            use_cache=use_cache,
            page_number=page_number,
            page_size=page_size,
            target=target,
        )

    async def _fetch_datasets_internal(
        self,
        page_number: int = 1,
        page_size: int = 20,
        target: str = "",
    ) -> TrendingResponse:
        """Internal implementation to fetch datasets via API."""
        try:
            url = f"{self.api_base_url}/datasets"

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://modelscope.cn/datasets",
            }

            params = {
                "PageSize": page_size,
                "PageNumber": page_number,
                "Target": target,
            }

            logger.info(
                f"Fetching ModelScope datasets via API (page={page_number}, size={page_size}, target={target})"
            )

            response = await self.http_client.get(url, params=params, headers=headers)

            if response.status_code != 200:
                logger.warning(f"ModelScope API returned status {response.status_code}")
                return self._create_response(
                    success=False,
                    data_type="datasets",
                    data=[],
                    error=f"HTTP {response.status_code}",
                )

            data = response.json()

            if data.get("Code") != 200:
                error_msg = data.get("Message", "Unknown error")
                logger.warning(f"ModelScope API error: {error_msg}")
                return self._create_response(
                    success=False,
                    data_type="datasets",
                    data=[],
                    error=error_msg,
                )

            # Parse datasets from response
            datasets = self._parse_datasets(data, page_size)

            total_count = data.get("TotalCount", len(datasets))

            return self._create_response(
                success=True,
                data_type="datasets",
                data=datasets,
                metadata={
                    "total_count": total_count,
                    "page_number": page_number,
                    "page_size": page_size,
                    "target": target,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching ModelScope datasets: {e}")
            return self._create_response(success=False, data_type="datasets", data=[], error=str(e))

    def _parse_models(
        self, response_data: dict[str, Any], limit: int
    ) -> list[ModelScopeModel]:
        """Parse models from ModelScope API response."""
        models = []
        rank = 1

        try:
            # Extract models from Data.Model.Models
            items = []
            if "Data" in response_data and isinstance(response_data["Data"], dict):
                if "Model" in response_data["Data"] and isinstance(response_data["Data"]["Model"], dict):
                    items = response_data["Data"]["Model"].get("Models", [])

            for item_data in items[:limit]:
                try:
                    # Parse timestamps
                    created_time = None
                    if "CreatedTime" in item_data:
                        try:
                            created_time = datetime.fromisoformat(
                                str(item_data["CreatedTime"]).replace("Z", "+00:00")
                            )
                        except (ValueError, AttributeError):
                            pass

                    last_updated = None
                    if "LastUpdatedTime" in item_data:
                        try:
                            last_updated = datetime.fromisoformat(
                                str(item_data["LastUpdatedTime"]).replace("Z", "+00:00")
                            )
                        except (ValueError, AttributeError):
                            pass

                    model_id = item_data.get("Id", "")
                    namespace = item_data.get("Namespace", "")
                    name = item_data.get("Name", model_id)

                    # Extract task from Tasks array (usually first item)
                    tasks = item_data.get("Tasks", [])
                    task = tasks[0] if tasks else None

                    # Extract frameworks
                    frameworks = item_data.get("Frameworks", [])
                    if not frameworks:
                        # Try alternative field names
                        frameworks = item_data.get("Libraries", [])

                    # Extract tags
                    tags = item_data.get("Tags", [])
                    if not tags:
                        tags = item_data.get("OfficialTags", [])

                    model = ModelScopeModel(
                        rank=rank,
                        id=model_id,
                        name=name,
                        namespace=namespace,
                        task=task,
                        description=item_data.get("Description"),
                        chinese_name=item_data.get("ChineseName"),
                        downloads=item_data.get("Downloads", 0),
                        likes=item_data.get("Likes", 0),
                        stars=item_data.get("Stars", 0),
                        tags=tags,
                        frameworks=frameworks,
                        url=f"https://modelscope.cn/models/{namespace}/{name}" if namespace and name else f"https://modelscope.cn/models/{model_id}",
                        gmt_create=created_time,
                        gmt_modified=last_updated,
                    )

                    models.append(model)
                    rank += 1

                except Exception as e:
                    logger.warning(f"Error parsing ModelScope model: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing ModelScope models response: {e}")

        return models

    def _parse_datasets(
        self, response_data: dict[str, Any], limit: int
    ) -> list[ModelScopeDataset]:
        """Parse datasets from ModelScope API response."""
        datasets = []
        rank = 1

        try:
            # Data is a direct array in the response
            items = response_data.get("Data", [])

            for item_data in items[:limit]:
                try:
                    # Parse timestamps (Unix timestamps)
                    gmt_create = None
                    if "GmtCreate" in item_data and item_data["GmtCreate"]:
                        try:
                            gmt_create = datetime.fromtimestamp(item_data["GmtCreate"])
                        except (ValueError, TypeError, OSError):
                            pass

                    gmt_modified = None
                    if "GmtModified" in item_data and item_data["GmtModified"]:
                        try:
                            gmt_modified = datetime.fromtimestamp(item_data["GmtModified"])
                        except (ValueError, TypeError, OSError):
                            pass

                    last_updated = None
                    if "LastUpdatedTime" in item_data and item_data["LastUpdatedTime"]:
                        try:
                            last_updated = datetime.fromtimestamp(item_data["LastUpdatedTime"])
                        except (ValueError, TypeError, OSError):
                            pass

                    dataset_id = item_data.get("Id", "")
                    namespace = item_data.get("Namespace", "")
                    name = item_data.get("Name", dataset_id)

                    # Extract tags (may be null or array)
                    tags = item_data.get("Tags", [])
                    if tags is None:
                        tags = []

                    # Extract task categories from tags
                    task_categories = []
                    if tags:
                        for tag in tags:
                            if isinstance(tag, dict):
                                task = tag.get("task")
                                if task and task not in task_categories:
                                    task_categories.append(task)

                    dataset = ModelScopeDataset(
                        rank=rank,
                        id=str(dataset_id),
                        name=name,
                        namespace=namespace,
                        description=item_data.get("Description"),
                        chinese_name=item_data.get("ChineseName"),
                        downloads=item_data.get("Downloads", 0),
                        likes=item_data.get("Likes", 0),
                        stars=item_data.get("Stars", 0),
                        tags=tags,
                        task_categories=task_categories,
                        url=f"https://modelscope.cn/datasets/{namespace}/{name}" if namespace and name else f"https://modelscope.cn/datasets/{dataset_id}",
                        gmt_create=gmt_create,
                        gmt_modified=gmt_modified or last_updated,
                    )

                    datasets.append(dataset)
                    rank += 1

                except Exception as e:
                    logger.warning(f"Error parsing ModelScope dataset: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing ModelScope datasets response: {e}")

        return datasets

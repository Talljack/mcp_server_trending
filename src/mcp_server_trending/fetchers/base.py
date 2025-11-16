"""Base fetcher class for all platform data fetchers."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models.base import TrendingResponse
from ..utils import HTTPClient, SimpleCache, logger


class BaseFetcher(ABC):
    """
    Abstract base class for all platform data fetchers.

    Provides common functionality for:
    - HTTP requests
    - Caching
    - Error handling
    - Response formatting
    """

    def __init__(
        self,
        cache: Optional[SimpleCache] = None,
        http_client: Optional[HTTPClient] = None,
        cache_ttl: int = 3600,
    ):
        """
        Initialize base fetcher.

        Args:
            cache: Cache instance (creates new if not provided)
            http_client: HTTP client instance (creates new if not provided)
            cache_ttl: Cache TTL in seconds (default: 1 hour)
        """
        self.cache = cache or SimpleCache(default_ttl=cache_ttl)
        self.http_client = http_client or HTTPClient()
        self.cache_ttl = cache_ttl
        self.platform_name = self.get_platform_name()

    @abstractmethod
    def get_platform_name(self) -> str:
        """
        Get platform name identifier.

        Returns:
            Platform name (e.g., 'github', 'producthunt')
        """
        pass

    def _get_cache_key(self, data_type: str, **params) -> str:
        """
        Generate cache key from data type and parameters.

        Args:
            data_type: Type of data being fetched
            **params: Additional parameters for cache key

        Returns:
            Cache key string
        """
        param_str = "_".join(f"{k}={v}" for k, v in sorted(params.items()) if v is not None)
        if param_str:
            return f"{self.platform_name}:{data_type}:{param_str}"
        return f"{self.platform_name}:{data_type}"

    def _get_cached_response(self, cache_key: str) -> Optional[TrendingResponse]:
        """
        Get cached response if available.

        Args:
            cache_key: Cache key

        Returns:
            Cached response or None
        """
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for {cache_key}")
            cached["cache_hit"] = True
            return TrendingResponse(**cached)
        return None

    def _cache_response(self, cache_key: str, response: TrendingResponse) -> None:
        """
        Cache response data.

        Args:
            cache_key: Cache key
            response: Response to cache
        """
        self.cache.set(cache_key, response.to_dict(), ttl=self.cache_ttl)
        logger.debug(f"Cached response for {cache_key}")

    def _create_response(
        self,
        success: bool,
        data_type: str,
        data: List[Any],
        metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> TrendingResponse:
        """
        Create standardized response.

        Args:
            success: Whether the request was successful
            data_type: Type of data
            data: List of data items
            metadata: Additional metadata
            error: Error message if failed

        Returns:
            TrendingResponse object
        """
        return TrendingResponse(
            success=success,
            platform=self.platform_name,
            data_type=data_type,
            timestamp=datetime.now(),
            cache_hit=False,
            data=data,
            metadata=metadata or {},
            error=error,
        )

    async def fetch_with_cache(
        self, data_type: str, fetch_func, use_cache: bool = True, **params
    ) -> TrendingResponse:
        """
        Generic fetch method with caching support.

        Args:
            data_type: Type of data being fetched
            fetch_func: Async function to fetch data
            use_cache: Whether to use cache
            **params: Parameters for fetch function and cache key

        Returns:
            TrendingResponse
        """
        cache_key = self._get_cache_key(data_type, **params)

        # Try cache first
        if use_cache:
            cached_response = self._get_cached_response(cache_key)
            if cached_response:
                return cached_response

        # Fetch fresh data
        try:
            logger.info(f"Fetching fresh data for {cache_key}")
            response = await fetch_func(**params)

            # Cache successful response
            if response.success and use_cache:
                self._cache_response(cache_key, response)

            return response

        except Exception as e:
            logger.error(f"Error fetching {cache_key}: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type=data_type,
                data=[],
                error=str(e),
            )

    async def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        if self.http_client:
            await self.http_client.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

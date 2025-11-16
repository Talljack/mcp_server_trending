"""HTTP client utility with retry and rate limiting."""

import asyncio
import time
from typing import Any
from urllib.parse import urljoin

import httpx

from .logger import logger


class HTTPClient:
    """
    Reusable HTTP client with retry logic and rate limiting.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        headers: dict[str, str] | None = None,
    ):
        """
        Initialize HTTP client.

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
            headers: Default headers for all requests
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.default_headers = headers or {}
        self._client: httpx.AsyncClient | None = None

        # Rate limiting
        self._last_request_time: float = 0
        self._min_request_interval: float = 0.1  # 100ms between requests

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    async def _wait_for_rate_limit(self) -> None:
        """Ensure minimum interval between requests."""
        now = time.time()
        time_since_last = now - self._last_request_time
        if time_since_last < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - time_since_last)
        self._last_request_time = time.time()

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """
        Perform GET request with retry logic.

        Args:
            url: URL to request (relative to base_url if set)
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments for httpx.get

        Returns:
            HTTP response

        Raises:
            httpx.HTTPError: If request fails after all retries
        """
        full_url = urljoin(self.base_url, url) if self.base_url else url
        merged_headers = {**self.default_headers, **(headers or {})}

        client = await self._get_client()

        for attempt in range(self.max_retries):
            try:
                await self._wait_for_rate_limit()

                logger.debug(f"GET {full_url} (attempt {attempt + 1}/{self.max_retries})")
                response = await client.get(
                    full_url, params=params, headers=merged_headers, **kwargs
                )
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} for {full_url}")
                if e.response.status_code == 429:  # Rate limited
                    wait_time = self.retry_delay * (2**attempt)
                    logger.info(f"Rate limited, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                elif e.response.status_code >= 500:  # Server error, retry
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                raise

            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Request error for {full_url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

        raise httpx.HTTPError(f"Failed after {self.max_retries} attempts")

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """
        Perform POST request with retry logic.

        Args:
            url: URL to request (relative to base_url if set)
            data: Form data to send
            json: JSON data to send
            headers: Additional headers
            **kwargs: Additional arguments for httpx.post

        Returns:
            HTTP response

        Raises:
            httpx.HTTPError: If request fails after all retries
        """
        full_url = urljoin(self.base_url, url) if self.base_url else url
        merged_headers = {**self.default_headers, **(headers or {})}

        client = await self._get_client()

        for attempt in range(self.max_retries):
            try:
                await self._wait_for_rate_limit()

                logger.debug(f"POST {full_url} (attempt {attempt + 1}/{self.max_retries})")
                response = await client.post(
                    full_url, data=data, json=json, headers=merged_headers, **kwargs
                )
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} for {full_url}")
                if e.response.status_code == 429:  # Rate limited
                    wait_time = self.retry_delay * (2**attempt)
                    logger.info(f"Rate limited, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                elif e.response.status_code >= 500:  # Server error, retry
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                raise

            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Request error for {full_url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

        raise httpx.HTTPError(f"Failed after {self.max_retries} attempts")

    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """
        Perform PUT request with retry logic.

        Args:
            url: URL to request (relative to base_url if set)
            data: Form data to send
            json: JSON data to send
            headers: Additional headers
            **kwargs: Additional arguments for httpx.put

        Returns:
            HTTP response

        Raises:
            httpx.HTTPError: If request fails after all retries
        """
        full_url = urljoin(self.base_url, url) if self.base_url else url
        merged_headers = {**self.default_headers, **(headers or {})}

        client = await self._get_client()

        for attempt in range(self.max_retries):
            try:
                await self._wait_for_rate_limit()

                logger.debug(f"PUT {full_url} (attempt {attempt + 1}/{self.max_retries})")
                response = await client.put(
                    full_url, data=data, json=json, headers=merged_headers, **kwargs
                )
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} for {full_url}")
                if e.response.status_code == 429:  # Rate limited
                    wait_time = self.retry_delay * (2**attempt)
                    logger.info(f"Rate limited, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                elif e.response.status_code >= 500:  # Server error, retry
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                raise

            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Request error for {full_url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

        raise httpx.HTTPError(f"Failed after {self.max_retries} attempts")

    async def get_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Perform GET request and return JSON response.

        Args:
            url: URL to request
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments for httpx.get

        Returns:
            Parsed JSON response
        """
        response = await self.get(url, params=params, headers=headers, **kwargs)
        return response.json()

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

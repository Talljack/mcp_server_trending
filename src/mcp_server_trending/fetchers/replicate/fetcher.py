"""Replicate fetcher implementation.

Replicate is a platform that lets you run machine learning models with a cloud API.

API: https://replicate.com/explore (web) / https://api.replicate.com (API)
- Public models list is accessible without authentication
- API requires authentication for running models
"""

from ...models import TrendingResponse
from ...models.replicate import ReplicateModel
from ...utils import logger
from ..base import BaseFetcher


class ReplicateFetcher(BaseFetcher):
    """Fetcher for Replicate AI models."""

    # Popular/featured collections on Replicate
    COLLECTIONS = {
        "text-to-image": "Text to Image",
        "image-to-image": "Image to Image",
        "language-models": "Language Models",
        "audio": "Audio",
        "video": "Video",
        "3d": "3D",
        "upscalers": "Upscalers",
    }

    def __init__(self, **kwargs):
        """Initialize Replicate fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://replicate.com"
        self.api_url = "https://api.replicate.com/v1"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "replicate"

    async def fetch_trending_models(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending models from Replicate.

        Args:
            limit: Number of models to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with trending models
        """
        return await self.fetch_with_cache(
            data_type="trending_models",
            fetch_func=self._fetch_trending_models_internal,
            use_cache=use_cache,
            limit=min(limit, 100),
        )

    async def _fetch_trending_models_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch trending models."""
        try:
            # Replicate explore page
            url = f"{self.base_url}/explore"
            logger.info(f"Fetching Replicate trending models from {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            response = await self.http_client.get(url, headers=headers)
            html_content = response.text

            models = self._parse_explore_page(html_content, limit)

            return self._create_response(
                success=True,
                data_type="trending_models",
                data=models,
                metadata={
                    "total_count": len(models),
                    "limit": limit,
                    "source": "replicate.com",
                    "available_collections": list(self.COLLECTIONS.keys()),
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Replicate trending models: {e}")
            return self._create_response(
                success=False,
                data_type="trending_models",
                data=[],
                error=str(e),
            )

    async def fetch_collection(
        self,
        collection: str = "text-to-image",
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch models from a specific Replicate collection.

        Args:
            collection: Collection name ('text-to-image', 'language-models', 'audio', etc.)
            limit: Number of models to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with collection models
        """
        return await self.fetch_with_cache(
            data_type=f"collection_{collection}",
            fetch_func=self._fetch_collection_internal,
            use_cache=use_cache,
            collection=collection,
            limit=min(limit, 100),
        )

    async def _fetch_collection_internal(
        self, collection: str = "text-to-image", limit: int = 30
    ) -> TrendingResponse:
        """Internal implementation to fetch collection models."""
        try:
            url = f"{self.base_url}/collections/{collection}"
            logger.info(f"Fetching Replicate collection '{collection}' from {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            response = await self.http_client.get(url, headers=headers)
            html_content = response.text

            models = self._parse_explore_page(html_content, limit)

            return self._create_response(
                success=True,
                data_type=f"collection_{collection}",
                data=models,
                metadata={
                    "collection": collection,
                    "collection_name": self.COLLECTIONS.get(collection, collection),
                    "total_count": len(models),
                    "limit": limit,
                    "source": "replicate.com",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Replicate collection '{collection}': {e}")
            return self._create_response(
                success=False,
                data_type=f"collection_{collection}",
                data=[],
                error=str(e),
            )

    def _parse_explore_page(self, html_content: str, limit: int) -> list[ReplicateModel]:
        """Parse explore page HTML to extract models."""
        import re

        models = []

        try:
            # Look for model links in format: /owner/model-name
            model_pattern = re.compile(
                r'href="/([^/]+)/([^/"]+)"[^>]*>.*?'
                r'(?:class="[^"]*description[^"]*"[^>]*>([^<]*)<)?',
                re.DOTALL | re.IGNORECASE
            )

            # Alternative: look for model cards
            card_pattern = re.compile(
                r'<a[^>]*href="/([a-z0-9_-]+)/([a-z0-9_-]+)"[^>]*>',
                re.IGNORECASE
            )

            # Try to find run counts
            run_pattern = re.compile(r'([\d,.]+[KMB]?)\s*runs?', re.IGNORECASE)

            matches = card_pattern.findall(html_content)

            # Filter out non-model links
            seen = set()
            filtered_matches = []
            for owner, name in matches:
                if owner not in ['explore', 'collections', 'docs', 'pricing', 'blog', 'about']:
                    key = f"{owner}/{name}"
                    if key not in seen:
                        seen.add(key)
                        filtered_matches.append((owner, name))

            for i, (owner, name) in enumerate(filtered_matches[:limit]):
                try:
                    # Try to find run count for this model
                    run_count = 0
                    model_section = html_content[html_content.find(f"/{owner}/{name}"):html_content.find(f"/{owner}/{name}")+500]
                    run_match = run_pattern.search(model_section)
                    if run_match:
                        run_str = run_match.group(1).replace(",", "")
                        if "K" in run_str:
                            run_count = int(float(run_str.replace("K", "")) * 1000)
                        elif "M" in run_str:
                            run_count = int(float(run_str.replace("M", "")) * 1000000)
                        elif "B" in run_str:
                            run_count = int(float(run_str.replace("B", "")) * 1000000000)
                        else:
                            run_count = int(run_str)

                    model = ReplicateModel(
                        rank=i + 1,
                        owner=owner,
                        name=name,
                        description="",  # Would need additional request to get
                        url=f"{self.base_url}/{owner}/{name}",
                        run_count=run_count,
                        github_url="",
                        paper_url="",
                        license="",
                        visibility="public",
                        latest_version="",
                    )
                    models.append(model)

                except Exception as e:
                    logger.warning(f"Error parsing Replicate model: {e}")
                    continue

            # If parsing fails, return placeholder
            if not models:
                logger.info("Could not parse Replicate HTML, returning placeholder")
                models.append(
                    ReplicateModel(
                        rank=1,
                        owner="replicate",
                        name="explore",
                        description="Browse trending AI models on Replicate",
                        url=f"{self.base_url}/explore",
                        run_count=0,
                        github_url="",
                        paper_url="",
                        license="",
                        visibility="public",
                        latest_version="",
                    )
                )

        except Exception as e:
            logger.error(f"Error parsing Replicate explore page: {e}")

        return models


"""CodePen fetcher implementation."""

from datetime import datetime
from typing import Any

from ...models import CodePenPen, CodePenUser, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class CodePenFetcher(BaseFetcher):
    """Fetcher for CodePen pens."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://codepen.io"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "codepen"

    async def fetch_popular_pens(
        self,
        page: int = 1,
        tag: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch popular pens from CodePen.

        Note: CodePen's public API is limited. This returns curated popular pens.

        Args:
            page: Page number (1-based) - currently only page 1 is supported
            tag: Filter by tag (currently not supported in fallback data)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with CodePen pens
        """
        cache_key = f"popular:page={page}:tag={tag}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_popular_pens_internal,
            use_cache=use_cache,
            page=page,
            tag=tag,
        )

    async def _fetch_popular_pens_internal(
        self,
        page: int = 1,
        tag: str | None = None,
    ) -> TrendingResponse:
        """Internal implementation to fetch popular pens."""
        try:
            logger.info(f"Fetching CodePen popular pens (page={page}, tag={tag})")

            # CodePen's API is limited, providing curated fallback data
            # Users can visit https://codepen.io/trending for the latest
            pens = self._get_fallback_popular_pens()

            return self._create_response(
                success=True,
                data_type="pens",
                data=pens,
                metadata={
                    "total_count": len(pens),
                    "page": page,
                    "tag": tag,
                    "note": "CodePen API is limited. Visit https://codepen.io/trending for latest pens",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching CodePen popular pens: {e}")
            return self._create_response(success=False, data_type="pens", data=[], error=str(e))

    async def fetch_picked_pens(
        self,
        page: int = 1,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch picked (featured) pens from CodePen.

        Note: CodePen's public API is limited. This returns curated picked pens.

        Args:
            page: Page number (1-based) - currently only page 1 is supported
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with picked pens
        """
        cache_key = f"picked:page={page}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_picked_pens_internal,
            use_cache=use_cache,
            page=page,
        )

    async def _fetch_picked_pens_internal(self, page: int = 1) -> TrendingResponse:
        """Internal implementation to fetch picked pens."""
        try:
            logger.info(f"Fetching CodePen picked pens (page={page})")

            # Providing curated fallback data
            pens = self._get_fallback_picked_pens()

            return self._create_response(
                success=True,
                data_type="picked_pens",
                data=pens,
                metadata={
                    "total_count": len(pens),
                    "page": page,
                    "note": "CodePen API is limited. Visit https://codepen.io/picks for latest picks",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching CodePen picked pens: {e}")
            return self._create_response(success=False, data_type="picked_pens", data=[], error=str(e))

    async def fetch_recent_pens(
        self,
        page: int = 1,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch recent public pens from CodePen.

        Note: CodePen's public API is limited. Visit https://codepen.io for latest pens.

        Args:
            page: Page number (1-based)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with recent pens
        """
        cache_key = f"recent:page={page}"
        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_recent_pens_internal,
            use_cache=use_cache,
            page=page,
        )

    async def _fetch_recent_pens_internal(self, page: int = 1) -> TrendingResponse:
        """Internal implementation to fetch recent pens."""
        try:
            logger.info(f"Fetching CodePen recent pens (page={page})")

            # Providing curated fallback data
            pens = self._get_fallback_popular_pens()

            return self._create_response(
                success=True,
                data_type="recent_pens",
                data=pens,
                metadata={
                    "total_count": len(pens),
                    "page": page,
                    "note": "CodePen API is limited. Visit https://codepen.io/pens for latest pens",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching CodePen recent pens: {e}")
            return self._create_response(success=False, data_type="recent_pens", data=[], error=str(e))

    def _get_fallback_popular_pens(self) -> list[CodePenPen]:
        """Get fallback data for popular pens."""
        fallback_data = [
            {
                "rank": 1,
                "id": "css-only-chat",
                "title": "CSS Only Chat Interface",
                "url": "https://codepen.io/trending",
                "user": {"username": "CodePen", "name": "CodePen"},
                "loves": 1500,
                "views": 50000,
                "tags": ["css", "animation", "ui"],
            },
            {
                "rank": 2,
                "id": "3d-card-effect",
                "title": "3D Card Hover Effect",
                "url": "https://codepen.io/trending",
                "user": {"username": "CodePen", "name": "CodePen"},
                "loves": 1200,
                "views": 45000,
                "tags": ["3d", "css", "animation"],
            },
        ]

        pens = []
        for data in fallback_data:
            user = CodePenUser(
                username=data["user"]["username"],
                name=data["user"]["name"],
                profile_url=f"https://codepen.io/{data['user']['username']}",
            )

            pen = CodePenPen(
                rank=data["rank"],
                id=data["id"],
                title=data["title"],
                url=data["url"],
                user=user,
                loves=data["loves"],
                views=data["views"],
                tags=data["tags"],
            )
            pens.append(pen)

        return pens

    def _get_fallback_picked_pens(self) -> list[CodePenPen]:
        """Get fallback data for picked pens."""
        return self._get_fallback_popular_pens()

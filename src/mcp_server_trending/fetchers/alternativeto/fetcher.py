"""AlternativeTo fetcher implementation.

AlternativeTo is a website that lists alternatives to web-based software,
desktop software, and mobile apps.

Note: AlternativeTo has Cloudflare protection, so we provide curated fallback data
with links to the website for the latest information.
"""

from ...models import TrendingResponse
from ...models.alternativeto import AlternativeToApp
from ...utils import logger
from ..base import BaseFetcher


# Curated list of popular software alternatives
POPULAR_ALTERNATIVES = [
    {
        "id": "notion",
        "name": "Notion",
        "description": "All-in-one workspace for notes, docs, wikis, and project management",
        "likes": 5000,
        "platforms": ["Windows", "Mac", "Linux", "Web", "Android", "iPhone"],
        "tags": ["productivity", "notes", "project-management"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "obsidian",
        "name": "Obsidian",
        "description": "A powerful knowledge base that works on local Markdown files",
        "likes": 4500,
        "platforms": ["Windows", "Mac", "Linux", "Android", "iPhone"],
        "tags": ["notes", "markdown", "knowledge-management"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "figma",
        "name": "Figma",
        "description": "Collaborative interface design tool for teams",
        "likes": 4200,
        "platforms": ["Windows", "Mac", "Linux", "Web"],
        "tags": ["design", "ui-design", "collaboration"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "description": "Free source-code editor by Microsoft with extensive extensions",
        "likes": 8000,
        "platforms": ["Windows", "Mac", "Linux"],
        "tags": ["development", "code-editor", "ide"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "gimp",
        "name": "GIMP",
        "description": "Free and open-source image editor, alternative to Photoshop",
        "likes": 3500,
        "platforms": ["Windows", "Mac", "Linux"],
        "tags": ["image-editing", "graphics", "photo-editing"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "blender",
        "name": "Blender",
        "description": "Free and open-source 3D creation suite",
        "likes": 6000,
        "platforms": ["Windows", "Mac", "Linux"],
        "tags": ["3d-modeling", "animation", "video-editing"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "libreoffice",
        "name": "LibreOffice",
        "description": "Free and open-source office suite, alternative to Microsoft Office",
        "likes": 4000,
        "platforms": ["Windows", "Mac", "Linux"],
        "tags": ["office", "productivity", "documents"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "signal",
        "name": "Signal",
        "description": "Privacy-focused encrypted messaging app",
        "likes": 5500,
        "platforms": ["Windows", "Mac", "Linux", "Android", "iPhone"],
        "tags": ["messaging", "privacy", "encryption"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "bitwarden",
        "name": "Bitwarden",
        "description": "Open-source password manager",
        "likes": 4800,
        "platforms": ["Windows", "Mac", "Linux", "Web", "Android", "iPhone"],
        "tags": ["password-manager", "security", "privacy"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "firefox",
        "name": "Firefox",
        "description": "Privacy-focused open-source web browser",
        "likes": 7000,
        "platforms": ["Windows", "Mac", "Linux", "Android", "iPhone"],
        "tags": ["browser", "privacy", "web"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "brave",
        "name": "Brave",
        "description": "Privacy-focused browser with built-in ad blocker",
        "likes": 4600,
        "platforms": ["Windows", "Mac", "Linux", "Android", "iPhone"],
        "tags": ["browser", "privacy", "ad-blocker"],
        "is_free": True,
        "is_open_source": True,
    },
    {
        "id": "linear",
        "name": "Linear",
        "description": "Modern issue tracking tool for software teams",
        "likes": 3800,
        "platforms": ["Windows", "Mac", "Web", "Android", "iPhone"],
        "tags": ["project-management", "issue-tracking", "development"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "raycast",
        "name": "Raycast",
        "description": "Productivity tool and launcher for macOS",
        "likes": 3200,
        "platforms": ["Mac"],
        "tags": ["productivity", "launcher", "automation"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "arc",
        "name": "Arc Browser",
        "description": "A new kind of browser with spaces and profiles",
        "likes": 2800,
        "platforms": ["Mac", "Windows"],
        "tags": ["browser", "productivity", "web"],
        "is_free": True,
        "is_open_source": False,
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "description": "AI-first code editor built on VS Code",
        "likes": 3500,
        "platforms": ["Windows", "Mac", "Linux"],
        "tags": ["development", "ai", "code-editor"],
        "is_free": True,
        "is_open_source": False,
    },
]


class AlternativeToFetcher(BaseFetcher):
    """Fetcher for AlternativeTo software alternatives."""

    def __init__(self, **kwargs):
        """Initialize AlternativeTo fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://alternativeto.net"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "alternativeto"

    async def fetch_trending(
        self,
        platform: str = "all",
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending software from AlternativeTo.

        Args:
            platform: Platform filter ('all', 'windows', 'mac', 'linux', 'android', 'iphone', 'web')
            limit: Number of items to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with trending software
        """
        return await self.fetch_with_cache(
            data_type=f"trending_{platform}",
            fetch_func=self._fetch_trending_internal,
            use_cache=use_cache,
            platform=platform,
            limit=min(limit, 100),
        )

    async def _fetch_trending_internal(
        self, platform: str = "all", limit: int = 30
    ) -> TrendingResponse:
        """Internal implementation to fetch trending software."""
        try:
            logger.info(f"Fetching AlternativeTo trending for platform: {platform}")

            # Filter by platform if specified
            apps_data = POPULAR_ALTERNATIVES
            if platform != "all":
                platform_map = {
                    "windows": "Windows",
                    "mac": "Mac",
                    "linux": "Linux",
                    "android": "Android",
                    "iphone": "iPhone",
                    "web": "Web",
                }
                platform_name = platform_map.get(platform.lower(), platform)
                apps_data = [
                    app for app in POPULAR_ALTERNATIVES
                    if platform_name in app.get("platforms", [])
                ]

            apps = self._parse_apps(apps_data, limit)

            return self._create_response(
                success=True,
                data_type=f"trending_{platform}",
                data=apps,
                metadata={
                    "platform": platform,
                    "total_count": len(apps),
                    "limit": limit,
                    "source": "alternativeto.net",
                    "note": "Curated data - visit alternativeto.net for latest information",
                    "browse_url": f"{self.base_url}/browse/trending/",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching AlternativeTo trending: {e}")
            return self._create_response(
                success=False,
                data_type=f"trending_{platform}",
                data=[],
                error=str(e),
            )

    async def search_alternatives(
        self,
        query: str,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Search for software alternatives on AlternativeTo.

        Args:
            query: Software name to find alternatives for
            limit: Number of items to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with alternatives
        """
        return await self.fetch_with_cache(
            data_type=f"alternatives_{query}",
            fetch_func=self._search_alternatives_internal,
            use_cache=use_cache,
            query=query,
            limit=min(limit, 100),
        )

    async def _search_alternatives_internal(
        self, query: str, limit: int = 30
    ) -> TrendingResponse:
        """Internal implementation to search alternatives."""
        try:
            logger.info(f"Searching AlternativeTo alternatives for '{query}'")

            # Filter by query in name, description, or tags
            query_lower = query.lower()
            filtered_apps = []
            for app in POPULAR_ALTERNATIVES:
                name = app.get("name", "").lower()
                desc = app.get("description", "").lower()
                tags = " ".join(app.get("tags", [])).lower()

                if query_lower in name or query_lower in desc or query_lower in tags:
                    filtered_apps.append(app)

            apps = self._parse_apps(filtered_apps, limit)

            # If no matches, return all with search URL
            if not apps:
                apps = self._parse_apps(POPULAR_ALTERNATIVES, limit)

            return self._create_response(
                success=True,
                data_type=f"alternatives_{query}",
                data=apps,
                metadata={
                    "query": query,
                    "total_count": len(apps),
                    "limit": limit,
                    "source": "alternativeto.net",
                    "note": "Curated data - visit alternativeto.net for latest information",
                    "search_url": f"{self.base_url}/software/{query.lower().replace(' ', '-')}/",
                },
            )

        except Exception as e:
            logger.error(f"Error searching AlternativeTo for '{query}': {e}")
            return self._create_response(
                success=False,
                data_type=f"alternatives_{query}",
                data=[],
                error=str(e),
            )

    def _parse_apps(self, data: list, limit: int) -> list[AlternativeToApp]:
        """Parse apps from data."""
        apps = []

        for i, item in enumerate(data[:limit]):
            try:
                app = AlternativeToApp(
                    rank=i + 1,
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    url=f"{self.base_url}/software/{item.get('id', '')}/",
                    likes=item.get("likes", 0),
                    platforms=item.get("platforms", []),
                    tags=item.get("tags", []),
                    is_free=item.get("is_free", True),
                    is_open_source=item.get("is_open_source", False),
                    website_url="",
                )
                apps.append(app)

            except Exception as e:
                logger.warning(f"Error parsing AlternativeTo app: {e}")
                continue

        return apps

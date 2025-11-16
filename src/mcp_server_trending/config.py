"""Configuration management for MCP Server Trending."""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""

    # Server settings
    log_level: str = "INFO"
    cache_ttl: int = 3600  # 1 hour default

    # GitHub settings (optional - for authenticated requests with higher rate limits)
    github_token: str | None = None

    # Product Hunt settings (optional - for API access)
    producthunt_api_key: str | None = None
    producthunt_api_secret: str | None = None

    # Rate limiting
    max_requests_per_minute: int = 60

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Returns:
            Config instance
        """
        return cls(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            github_token=os.getenv("GITHUB_TOKEN"),
            producthunt_api_key=os.getenv("PRODUCTHUNT_API_KEY"),
            producthunt_api_secret=os.getenv("PRODUCTHUNT_API_SECRET"),
            max_requests_per_minute=int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")),
        )


# Global config instance
config = Config.from_env()

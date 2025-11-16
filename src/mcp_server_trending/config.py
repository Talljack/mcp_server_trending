"""Configuration management for MCP Server Trending."""

import os
from dataclasses import dataclass
from pathlib import Path


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

    # OpenRouter settings (optional - for API access)
    openrouter_api_key: str | None = None

    # HuggingFace settings (optional - for API access)
    huggingface_token: str | None = None

    # Rate limiting
    max_requests_per_minute: int = 60

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Environment variables take precedence over default values.

        Returns:
            Config instance
        """
        # Load .env file if it exists
        cls._load_dotenv()

        # Get default instance first (includes any hardcoded tokens)
        instance = cls()

        # Override with environment variables if present
        return cls(
            log_level=os.getenv("LOG_LEVEL", instance.log_level),
            cache_ttl=int(os.getenv("CACHE_TTL", str(instance.cache_ttl))),
            github_token=os.getenv("GITHUB_TOKEN", instance.github_token),
            producthunt_api_key=os.getenv("PRODUCTHUNT_API_KEY", instance.producthunt_api_key),
            producthunt_api_secret=os.getenv(
                "PRODUCTHUNT_API_SECRET", instance.producthunt_api_secret
            ),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", instance.openrouter_api_key),
            huggingface_token=os.getenv("HUGGINGFACE_TOKEN", instance.huggingface_token),
            max_requests_per_minute=int(
                os.getenv("MAX_REQUESTS_PER_MINUTE", str(instance.max_requests_per_minute))
            ),
        )

    @staticmethod
    def _load_dotenv():
        """Load .env file from project root if it exists."""
        # Try to find .env file
        current = Path(__file__).resolve()
        for parent in [current.parent] + list(current.parents):
            env_file = parent / ".env"
            if env_file.exists():
                # Simple .env file parser (避免额外依赖)
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            # Only set if not already in environment
                            if key.strip() not in os.environ:
                                os.environ[key.strip()] = value.strip()
                break


# Global config instance
config = Config.from_env()

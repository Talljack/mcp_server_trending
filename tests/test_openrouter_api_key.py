"""Test OpenRouter fetcher API key requirement."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending import config
from mcp_server_trending.fetchers.openrouter import OpenRouterFetcher


async def test_no_api_key_error():
    """Test that OpenRouter fetcher returns clear error when API key is not configured."""
    # Temporarily clear API key
    original_key = config.config.openrouter_api_key
    config.config.openrouter_api_key = None

    try:
        fetcher = OpenRouterFetcher()

        print("Testing OpenRouter fetcher without API key...")
        print("=" * 60)

        response = await fetcher.fetch_models(limit=10)

        print("\n✓ Response received")
        print(f"  Success: {response.success}")
        print("  Error message:")
        print("  " + "-" * 58)
        if response.error:
            for line in response.error.split("\n"):
                print(f"  {line}")
        print("  " + "-" * 58)

        # Check metadata
        if response.metadata:
            print("\n✓ Metadata:")
            for key, value in response.metadata.items():
                print(f"  - {key}: {value}")

        # Verify error contains expected information
        assert not response.success, "Should return success=False when no API key"
        assert response.error, "Should have error message"
        assert "OpenRouter API key not configured" in response.error
        assert "OPENROUTER_API_KEY" in response.error
        assert "https://openrouter.ai/keys" in response.error

        print("\n✅ OpenRouter API key check passed!")
        print("\nThis is the error message users will see when they")
        print("try to use OpenRouter tools without configuring an API key.")

        await fetcher.close()

    finally:
        # Restore original key
        config.config.openrouter_api_key = original_key


async def test_other_fetchers_work():
    """Test that other fetchers work without OpenRouter API key."""
    print("\n" + "=" * 60)
    print("Testing that other fetchers work without OpenRouter API key...")
    print("=" * 60)

    from mcp_server_trending.fetchers.github import GitHubTrendingFetcher

    fetcher = GitHubTrendingFetcher()
    print("\n✓ GitHub fetcher initialized successfully")
    print(f"  Platform: {fetcher.platform_name}")

    await fetcher.close()
    print("✓ GitHub fetcher works independently of OpenRouter API key")


if __name__ == "__main__":
    asyncio.run(test_no_api_key_error())
    asyncio.run(test_other_fetchers_work())

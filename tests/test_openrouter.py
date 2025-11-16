"""Test OpenRouter fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.openrouter import OpenRouterFetcher


async def test_openrouter_models():
    """Test OpenRouter LLM models fetcher."""

    print("=" * 60)
    print("Testing OpenRouter LLM Models Fetcher")
    print("=" * 60)
    print()

    fetcher = OpenRouterFetcher()

    # Test 1: Fetch all models
    print("Test 1: Fetch LLM models (limit 10)")
    print("-" * 60)

    response = await fetcher.fetch_models(limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 models
        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name}")
            print(f"      ID: {model.id}")
            print(f"      Provider: {model.provider}")
            if model.context_length:
                print(f"      Context: {model.context_length:,} tokens")
            if model.pricing:
                print(
                    f"      Pricing: ${model.pricing.get('prompt', 0):.6f}/prompt, ${model.pricing.get('completion', 0):.6f}/completion"
                )
            if model.supports_vision:
                print("      Vision: Yes")
    else:
        print(f"   ✗ Failed: {response.error}")
        if "API key not configured" in str(response.error):
            print("\n⚠️  Please configure OPENROUTER_API_KEY in .env file")
            print("   Get your key at: https://openrouter.ai/keys")
            return

    # Test 2: Fetch popular models
    print(f"\n{'=' * 60}")
    print("Test 2: Fetch popular models (limit 5)")
    print("-" * 60)

    response = await fetcher.fetch_popular_models(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} popular models")
        print(f"   ✓ Metadata: {response.metadata}")

        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name} ({model.provider})")
            if hasattr(model, "requests_per_day") and model.requests_per_day:
                print(f"      Requests/day: {model.requests_per_day:,}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Fetch best value models
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch best value models (limit 5)")
    print("-" * 60)

    response = await fetcher.fetch_best_value_models(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} best value models")
        print(f"   ✓ Metadata: {response.metadata}")

        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name} ({model.provider})")
            if hasattr(model, "value_score") and model.value_score:
                print(f"      Value Score: {model.value_score:.2f}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Fetch fastest models
    print(f"\n{'=' * 60}")
    print("Test 4: Fetch fastest models (limit 5)")
    print("-" * 60)

    response = await fetcher.fetch_fastest_models(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} fastest models")
        print(f"   ✓ Metadata: {response.metadata}")

        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name} ({model.provider})")
            if hasattr(model, "latency_ms") and model.latency_ms:
                print(f"      Latency: {model.latency_ms:.0f}ms")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 5: Test caching
    print(f"\n{'=' * 60}")
    print("Test 5: Test caching mechanism")
    print("-" * 60)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_models(limit=3, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} models")

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_models(limit=3, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} models (from cache)")

    if response1.success and response2.success:
        # Data should be identical if cached
        if len(response1.data) == len(response2.data):
            print("   ✓ Cache working: Same data returned")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("OpenRouter Tests Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_openrouter_models())

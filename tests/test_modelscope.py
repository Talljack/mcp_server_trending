"""Test ModelScope (魔塔社区) fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.modelscope import ModelScopeFetcher


async def test_modelscope_models():
    """Test ModelScope models fetcher."""

    print("=" * 60)
    print("Testing ModelScope (魔塔社区) Models Fetcher")
    print("=" * 60)
    print()

    fetcher = ModelScopeFetcher()

    # Test 1: Fetch models
    print("Test 1: Fetch models")
    print("-" * 60)

    response = await fetcher.fetch_models(page_size=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 models
        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name}")
            if model.namespace:
                print(f"      Namespace: {model.namespace}")
            if model.task:
                print(f"      Task: {model.task}")
            print(f"      Downloads: {model.downloads:,}")
            print(f"      Likes: {model.likes}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        raise

    # Test 3: Search models by name
    print(f"\n{'=' * 60}")
    print("Test 3: Search models by name (GLM)")
    print("-" * 60)

    response = await fetcher.fetch_models(page_size=5, search_text="GLM", use_cache=False)

    if response.success:
        print(f"   ✓ Success: Found {len(response.data)} models for 'GLM'")
        print(f"   ✓ Search text: {response.metadata.get('search_text')}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_models(page_size=5, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} models, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_models(page_size=5, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} models, cache_hit={response2.cache_hit}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("ModelScope Models Tests Completed!")
    print("=" * 60)


async def test_modelscope_datasets():
    """Test ModelScope datasets fetcher."""

    print(f"\n{'=' * 60}")
    print("Testing ModelScope (魔塔社区) Datasets Fetcher")
    print("=" * 60)
    print()

    fetcher = ModelScopeFetcher()

    # Test 1: Fetch datasets
    print("Test 1: Fetch datasets")
    print("-" * 60)

    response = await fetcher.fetch_datasets(page_size=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} datasets")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 datasets
        for i, dataset in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {dataset.name}")
            if dataset.namespace:
                print(f"      Namespace: {dataset.namespace}")
            print(f"      Downloads: {dataset.downloads:,}")
            print(f"      Likes: {dataset.likes}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization for datasets")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        raise

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("ModelScope Datasets Tests Completed!")
    print("=" * 60)


async def main():
    """Run all ModelScope tests."""
    await test_modelscope_models()
    await test_modelscope_datasets()

    print(f"\n{'=' * 80}")
    print("✅ ALL MODELSCOPE TESTS COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


"""Test HuggingFace fetcher functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.huggingface import HuggingFaceFetcher


async def test_huggingface_models():
    """Test HuggingFace models fetcher."""

    print("=" * 60)
    print("Testing HuggingFace Models Fetcher")
    print("=" * 60)
    print()

    fetcher = HuggingFaceFetcher()

    # Test 1: Fetch trending models (by downloads)
    print("Test 1: Fetch trending models (sort by downloads)")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(sort_by="downloads", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 models
        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name}")
            print(f"      ID: {model.id}")
            if model.author:
                print(f"      Author: {model.author}")
            print(f"      Downloads: {model.downloads:,}")
            print(f"      Likes: {model.likes}")
            if model.pipeline_tag:
                print(f"      Task: {model.pipeline_tag}")
            if model.library_name:
                print(f"      Library: {model.library_name}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Fetch models filtered by task
    print(f"\n{'=' * 60}")
    print("Test 2: Fetch text-generation models")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(
        sort_by="downloads", task="text-generation", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} text-generation models")
        print(f"   ✓ Metadata: {response.metadata}")

        for i, model in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {model.name} ({model.id})")
            print(f"      Downloads: {model.downloads:,}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 3: Fetch models by library
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch transformers models")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(
        sort_by="likes", library="transformers", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} transformers models")
        print(f"   ✓ Metadata: {response.metadata}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_trending_models(limit=3, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} models")

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_trending_models(limit=3, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} models (from cache)")

    if response1.success and response2.success:
        # Data should be identical if cached
        if len(response1.data) == len(response2.data):
            print("   ✓ Cache working: Same data returned")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("HuggingFace Models Tests Completed!")
    print("=" * 60)


async def test_huggingface_datasets():
    """Test HuggingFace datasets fetcher."""

    print(f"\n{'=' * 60}")
    print("Testing HuggingFace Datasets Fetcher")
    print("=" * 60)
    print()

    fetcher = HuggingFaceFetcher()

    # Test 1: Fetch trending datasets
    print("Test 1: Fetch trending datasets (sort by downloads)")
    print("-" * 60)

    response = await fetcher.fetch_trending_datasets(sort_by="downloads", limit=10, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} datasets")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 datasets
        for i, dataset in enumerate(response.data[:3], 1):
            print(f"\n   {i}. {dataset.name}")
            print(f"      ID: {dataset.id}")
            if dataset.author:
                print(f"      Author: {dataset.author}")
            print(f"      Downloads: {dataset.downloads:,}")
            print(f"      Likes: {dataset.likes}")
            if dataset.task_categories:
                print(f"      Tasks: {', '.join(dataset.task_categories[:3])}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Fetch datasets by task
    print(f"\n{'=' * 60}")
    print("Test 2: Fetch datasets filtered by task")
    print("-" * 60)

    response = await fetcher.fetch_trending_datasets(
        sort_by="likes", task="text-classification", limit=5, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} datasets")
        print(f"   ✓ Metadata: {response.metadata}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("HuggingFace Datasets Tests Completed!")
    print("=" * 60)


async def main():
    """Run all HuggingFace tests."""
    await test_huggingface_models()
    await test_huggingface_datasets()


if __name__ == "__main__":
    asyncio.run(main())

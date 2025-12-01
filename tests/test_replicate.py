"""Test Replicate fetcher functionality."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.replicate import ReplicateFetcher


async def test_replicate_trending():
    """Test Replicate trending models fetcher."""

    print("=" * 60)
    print("Testing Replicate Trending Models Fetcher")
    print("=" * 60)
    print()

    fetcher = ReplicateFetcher()

    # Test 1: Fetch trending models
    print("Test 1: Fetch trending models (default limit)")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(limit=15, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Data Type: {response.data_type}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show top 3 models
        for i, model in enumerate(response.data[:3], 1):
            model_dict = model.to_dict()
            print(f"\n   {i}. {model_dict['full_name']}")
            print(f"      Rank: {model_dict['rank']}")
            print(f"      URL: {model_dict['url']}")
            if model_dict['run_count'] > 0:
                print(f"      Run Count: {model_dict['run_count']:,}")
            if model_dict['description']:
                desc = (
                    model_dict['description'][:80] + "..."
                    if len(model_dict['description']) > 80
                    else model_dict['description']
                )
                print(f"      Description: {desc}")
            if model_dict['license']:
                print(f"      License: {model_dict['license']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 2: Test JSON serialization (critical for MCP server)
    print(f"\n{'=' * 60}")
    print("Test 2: Test JSON serialization")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
        print(f"   ✓ Models in JSON: {len(response_dict.get('data', []))}")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        raise

    # Test 3: Fetch with small limit
    print(f"\n{'=' * 60}")
    print("Test 3: Fetch with small limit (5 models)")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} models")
        assert len(response.data) <= 5, "Should respect limit parameter"
        print(f"   ✓ Limit respected: {len(response.data)} <= 5")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Test caching
    print(f"\n{'=' * 60}")
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    # First fetch (should not use cache)
    response1 = await fetcher.fetch_trending_models(limit=10, use_cache=True)
    print(f"   ✓ First fetch: {len(response1.data)} models")
    print(f"   ✓ Cache hit: {response1.cache_hit}")

    # Second fetch (should use cache)
    response2 = await fetcher.fetch_trending_models(limit=10, use_cache=True)
    print(f"   ✓ Second fetch: {len(response2.data)} models")
    print(f"   ✓ Cache hit: {response2.cache_hit} (should be True)")

    if response1.success and response2.success:
        # Data should be identical if cached
        if len(response1.data) == len(response2.data):
            print("   ✓ Cache working: Same data returned")

    # Test 5: Test with cache disabled
    print(f"\n{'=' * 60}")
    print("Test 5: Test with cache disabled")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(limit=5, use_cache=False)
    print(f"   ✓ Fetched: {len(response.data)} models")
    print(f"   ✓ Cache hit: {response.cache_hit} (should be False)")
    assert not response.cache_hit, "Should not use cache when disabled"

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Replicate Trending Models Tests Completed!")
    print("=" * 60)


async def test_replicate_collections():
    """Test Replicate collections fetcher."""

    print(f"\n{'=' * 60}")
    print("Testing Replicate Collections Fetcher")
    print("=" * 60)
    print()

    fetcher = ReplicateFetcher()

    # Test available collections
    collections = [
        ("text-to-image", "Text to Image"),
        ("image-to-image", "Image to Image"),
        ("language-models", "Language Models"),
        ("audio", "Audio"),
        ("video", "Video"),
    ]

    for collection_id, collection_name in collections:
        print(f"Test: Fetch {collection_name} collection")
        print("-" * 60)

        response = await fetcher.fetch_collection(
            collection=collection_id, limit=5, use_cache=False
        )

        if response.success:
            print(f"   ✓ Success: Fetched {len(response.data)} models")
            print(f"   ✓ Data Type: {response.data_type}")
            print(f"   ✓ Collection: {response.metadata.get('collection')}")
            print(f"   ✓ Collection Name: {response.metadata.get('collection_name')}")

            # Test JSON serialization for collections
            try:
                response_dict = response.to_dict()
                json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
                print(f"   ✓ JSON serialization successful")
            except Exception as e:
                print(f"   ✗ JSON serialization failed: {e}")
                raise

            # Show first model
            if response.data:
                model = response.data[0]
                model_dict = model.to_dict()
                print(f"   ✓ First model: {model_dict['full_name']}")
        else:
            print(f"   ✗ Failed: {response.error}")

        print()

    # Cleanup
    await fetcher.close()

    print(f"{'=' * 60}")
    print("Replicate Collections Tests Completed!")
    print("=" * 60)


async def test_replicate_text_to_image():
    """Test Replicate text-to-image collection in detail."""

    print(f"\n{'=' * 60}")
    print("Testing Replicate Text-to-Image Collection (Detailed)")
    print("=" * 60)
    print()

    fetcher = ReplicateFetcher()

    print("Test: Fetch text-to-image models")
    print("-" * 60)

    response = await fetcher.fetch_collection(
        collection="text-to-image", limit=10, use_cache=False
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} text-to-image models")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show all models
        for i, model in enumerate(response.data, 1):
            model_dict = model.to_dict()
            print(f"\n   {i}. {model_dict['full_name']}")
            print(f"      URL: {model_dict['url']}")
            if model_dict['run_count'] > 0:
                print(f"      Runs: {model_dict['run_count']:,}")

        # Test caching for collections
        print(f"\n{'=' * 60}")
        print("Test: Collection caching")
        print("-" * 60)

        response_cached = await fetcher.fetch_collection(
            collection="text-to-image", limit=10, use_cache=True
        )
        print(f"   ✓ Cache hit: {response_cached.cache_hit}")

    else:
        print(f"   ✗ Failed: {response.error}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Text-to-Image Collection Tests Completed!")
    print("=" * 60)


async def test_replicate_metadata():
    """Test Replicate metadata and response structure."""

    print(f"\n{'=' * 60}")
    print("Testing Replicate Metadata and Response Structure")
    print("=" * 60)
    print()

    fetcher = ReplicateFetcher()

    print("Test: Verify response structure and metadata")
    print("-" * 60)

    response = await fetcher.fetch_trending_models(limit=5, use_cache=False)

    if response.success:
        print(f"   ✓ Response success: {response.success}")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Data type: {response.data_type}")
        print(f"   ✓ Timestamp: {response.timestamp}")
        print(f"   ✓ Cache hit: {response.cache_hit}")
        print(f"   ✓ Error: {response.error}")

        # Check metadata
        print(f"\n   Metadata:")
        for key, value in response.metadata.items():
            print(f"      - {key}: {value}")

        # Verify required metadata fields
        required_fields = ["total_count", "limit", "source", "available_collections"]
        for field in required_fields:
            assert field in response.metadata, f"Missing required field: {field}"
            print(f"   ✓ Required field present: {field}")

        # Check available collections
        collections = response.metadata.get("available_collections", [])
        print(f"\n   Available collections ({len(collections)}):")
        for collection in collections:
            print(f"      - {collection}")

        # Verify model structure
        if response.data:
            print(f"\n   Model structure verification:")
            model = response.data[0]
            model_dict = model.to_dict()
            required_model_fields = [
                "rank",
                "owner",
                "name",
                "full_name",
                "description",
                "url",
                "run_count",
            ]
            for field in required_model_fields:
                assert field in model_dict, f"Missing required model field: {field}"
                print(f"      ✓ Model field present: {field}")

    else:
        print(f"   ✗ Failed: {response.error}")

    # Cleanup
    await fetcher.close()

    print(f"\n{'=' * 60}")
    print("Metadata Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Replicate tests."""
    await test_replicate_trending()
    await test_replicate_collections()
    await test_replicate_text_to_image()
    await test_replicate_metadata()

    print(f"\n{'=' * 80}")
    print("✅ ALL REPLICATE TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


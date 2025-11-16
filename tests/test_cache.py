"""Tests for cache functionality."""

import sys
import os
import time
import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import SimpleCache


def test_cache_set_and_get():
    """Test basic cache set and get."""
    cache = SimpleCache(default_ttl=60)

    # Set value
    cache.set("test_key", "test_value")

    # Get value
    value = cache.get("test_key")
    assert value == "test_value"


def test_cache_expiry():
    """Test cache expiration."""
    cache = SimpleCache(default_ttl=1)  # 1 second TTL

    # Set value
    cache.set("test_key", "test_value")

    # Immediately get should work
    assert cache.get("test_key") == "test_value"

    # Wait for expiry
    time.sleep(1.1)

    # Should be expired
    assert cache.get("test_key") is None


def test_cache_delete():
    """Test cache deletion."""
    cache = SimpleCache()

    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

    # Delete
    deleted = cache.delete("test_key")
    assert deleted is True
    assert cache.get("test_key") is None

    # Delete non-existent
    deleted = cache.delete("non_existent")
    assert deleted is False


def test_cache_clear():
    """Test cache clear."""
    cache = SimpleCache()

    cache.set("key1", "value1")
    cache.set("key2", "value2")

    cache.clear()

    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_cache_stats():
    """Test cache statistics."""
    cache = SimpleCache(default_ttl=1)

    cache.set("key1", "value1")
    cache.set("key2", "value2", ttl=10)

    stats = cache.stats()
    assert stats["total_entries"] == 2
    assert stats["active_entries"] == 2

    # Wait for one to expire
    time.sleep(1.1)

    stats = cache.stats()
    assert stats["total_entries"] == 2
    assert stats["active_entries"] == 1


def test_cache_cleanup():
    """Test cache cleanup of expired entries."""
    cache = SimpleCache(default_ttl=1)

    cache.set("key1", "value1")
    cache.set("key2", "value2", ttl=10)

    # Wait for first to expire
    time.sleep(1.1)

    # Cleanup expired
    removed = cache.cleanup_expired()
    assert removed == 1

    # Only one entry should remain
    stats = cache.stats()
    assert stats["total_entries"] == 1

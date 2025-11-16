"""Tests for data models."""

import sys
import os
from datetime import datetime
from dataclasses import dataclass

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_server_trending.models import (
    BaseModel,
    TrendingResponse,
    GitHubRepository,
    GitHubDeveloper,
    HackerNewsStory,
    ProductHuntProduct,
)


def test_base_model_to_dict():
    """Test BaseModel to_dict conversion."""

    @dataclass
    class TestModel(BaseModel):
        name: str
        value: int

    model = TestModel(name="test", value=123)
    data = model.to_dict()

    assert data["name"] == "test"
    assert data["value"] == 123


def test_trending_response():
    """Test TrendingResponse model."""
    response = TrendingResponse(
        success=True, platform="github", data_type="trending_repos", data=[], metadata={"count": 0}
    )

    assert response.success is True
    assert response.platform == "github"
    assert response.data_type == "trending_repos"
    assert isinstance(response.timestamp, datetime)

    # Test to_dict
    data = response.to_dict()
    assert data["success"] is True
    assert data["platform"] == "github"


def test_github_repository():
    """Test GitHubRepository model."""
    repo = GitHubRepository(
        rank=1,
        author="test_author",
        name="test_repo",
        url="https://github.com/test_author/test_repo",
        description="Test repository",
        language="Python",
        stars=100,
        forks=20,
        stars_today=5,
        built_by=["user1", "user2"],
    )

    assert repo.rank == 1
    assert repo.author == "test_author"
    assert repo.language == "Python"

    # Test to_dict
    data = repo.to_dict()
    assert data["author"] == "test_author"
    assert data["stars"] == 100


def test_github_developer():
    """Test GitHubDeveloper model."""
    dev = GitHubDeveloper(
        rank=1,
        username="test_user",
        name="Test User",
        url="https://github.com/test_user",
        avatar="https://avatars.githubusercontent.com/u/123",
    )

    assert dev.username == "test_user"
    assert dev.name == "Test User"

    data = dev.to_dict()
    assert data["username"] == "test_user"


def test_hackernews_story():
    """Test HackerNewsStory model."""
    story = HackerNewsStory(
        rank=1,
        id=12345,
        title="Test Story",
        url="https://example.com",
        score=100,
        author="test_author",
        time=datetime.now(),
        descendants=50,
        story_type="story",
    )

    assert story.id == 12345
    assert story.title == "Test Story"
    assert story.score == 100

    data = story.to_dict()
    assert data["id"] == 12345
    assert isinstance(data["time"], str)  # Should be ISO format


def test_producthunt_product():
    """Test ProductHuntProduct model."""
    product = ProductHuntProduct(
        rank=1,
        name="Test Product",
        tagline="A test product",
        url="https://producthunt.com/posts/test",
        product_url="https://example.com",
        votes=100,
        comments_count=20,
        topics=["Developer Tools", "AI"],
        makers=[],
    )

    assert product.name == "Test Product"
    assert product.votes == 100
    assert "AI" in product.topics

    data = product.to_dict()
    assert data["name"] == "Test Product"
    assert len(data["topics"]) == 2

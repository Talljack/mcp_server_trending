"""Tests for Twitter/X fetcher using Nitter."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.fetchers.twitter import TwitterFetcher
from mcp_server_trending.utils import SimpleCache, setup_logger


async def test_twitter_hashtag():
    """Test fetching tweets by hashtag."""
    print("=" * 60)
    print("Testing Twitter/X Hashtag Fetcher (via Nitter)")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    # Test 1: Fetch #buildinpublic tweets
    print("\nTest 1: Fetch #buildinpublic tweets")
    print("-" * 60)

    response = await fetcher.fetch_hashtag_tweets(
        hashtag="buildinpublic",
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tweets")
        print(f"   ✓ Platform: {response.platform}")
        print(f"   ✓ Metadata: {response.metadata}")

        # Show first 3 tweets
        for tweet in response.data[:3]:
            tweet_dict = tweet.to_dict()
            print(f"\n   {tweet_dict['rank']}. @{tweet_dict['author']['username']}")
            content = tweet_dict['content'][:100] + "..." if len(tweet_dict['content']) > 100 else tweet_dict['content']
            print(f"      {content}")
            print(f"      ❤️ {tweet_dict['stats']['likes']} | 🔁 {tweet_dict['stats']['retweets']} | 💬 {tweet_dict['stats']['replies']}")
    else:
        print(f"   ✗ Failed: {response.error}")
        print("   Note: Nitter instances may be temporarily unavailable")

    # Test 2: JSON serialization
    print("\n" + "=" * 60)
    print("Test 2: Test JSON serialization")
    print("-" * 60)

    try:
        response_dict = response.to_dict()
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        print(f"   ✓ JSON serialization successful")
        print(f"   ✓ JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")

    # Test 3: Fetch #indiehackers tweets
    print("\n" + "=" * 60)
    print("Test 3: Fetch #indiehackers tweets")
    print("-" * 60)

    response = await fetcher.fetch_hashtag_tweets(
        hashtag="indiehackers",
        limit=5,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tweets")
        print(f"   ✓ Hashtag: indiehackers")
    else:
        print(f"   ✗ Failed: {response.error}")

    # Test 4: Caching mechanism
    print("\n" + "=" * 60)
    print("Test 4: Test caching mechanism")
    print("-" * 60)

    response1 = await fetcher.fetch_hashtag_tweets(
        hashtag="saas",
        limit=5,
        use_cache=True,
    )
    print(f"   ✓ First fetch: {len(response1.data)} tweets, cache_hit={response1.cache_hit}")

    response2 = await fetcher.fetch_hashtag_tweets(
        hashtag="saas",
        limit=5,
        use_cache=True,
    )
    print(f"   ✓ Second fetch: {len(response2.data)} tweets, cache_hit={response2.cache_hit}")

    print("\n" + "=" * 60)
    print("Twitter Hashtag Tests Completed!")
    print("=" * 60)


async def test_twitter_user_tweets():
    """Test fetching tweets from a specific user."""
    print("\n" + "=" * 60)
    print("Testing Twitter/X User Tweets Fetcher")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    # Test: Fetch tweets from @levelsio (Pieter Levels)
    print("\nTest: Fetch tweets from @levelsio")
    print("-" * 60)

    response = await fetcher.fetch_user_tweets(
        username="levelsio",
        limit=5,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tweets from @levelsio")
        print(f"   ✓ Metadata: {response.metadata}")

        for tweet in response.data[:3]:
            tweet_dict = tweet.to_dict()
            content = tweet_dict['content'][:80] + "..." if len(tweet_dict['content']) > 80 else tweet_dict['content']
            print(f"\n   - {content}")
            print(f"     ❤️ {tweet_dict['stats']['likes']} | 🔁 {tweet_dict['stats']['retweets']}")
    else:
        print(f"   ✗ Failed: {response.error}")
        print("   Note: User may be private or Nitter instance unavailable")

    print("\n" + "=" * 60)
    print("Twitter User Tweets Tests Completed!")
    print("=" * 60)


async def test_twitter_tech_tweets():
    """Test fetching aggregated tech tweets."""
    print("\n" + "=" * 60)
    print("Testing Twitter/X Tech Tweets Aggregation")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    # Test: Fetch tech tweets from multiple hashtags
    print("\nTest: Fetch aggregated tech tweets")
    print("-" * 60)

    response = await fetcher.fetch_tech_tweets(
        limit=15,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tech tweets")
        print(f"   ✓ Hashtags searched: {response.metadata.get('hashtags_searched', [])}")

        # Show top 5 by engagement
        print("\n   Top tweets by engagement:")
        for tweet in response.data[:5]:
            tweet_dict = tweet.to_dict()
            engagement = tweet_dict['stats']['likes'] + tweet_dict['stats']['retweets']
            content = tweet_dict['content'][:60] + "..." if len(tweet_dict['content']) > 60 else tweet_dict['content']
            print(f"\n   {tweet_dict['rank']}. @{tweet_dict['author']['username']} (engagement: {engagement})")
            print(f"      {content}")
            if tweet_dict['hashtags']:
                print(f"      Tags: #{' #'.join(tweet_dict['hashtags'][:3])}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Twitter Tech Tweets Tests Completed!")
    print("=" * 60)


async def test_twitter_indie_hackers():
    """Test fetching tweets from indie hacker influencers."""
    print("\n" + "=" * 60)
    print("Testing Twitter/X Indie Hackers Tweets")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    # Test: Fetch tweets from indie hacker influencers
    print("\nTest: Fetch tweets from indie hacker influencers")
    print("-" * 60)

    response = await fetcher.fetch_indie_hackers_tweets(
        limit=10,
        use_cache=False,
    )

    if response.success:
        print(f"   ✓ Success: Fetched {len(response.data)} tweets")
        print(f"   ✓ Influencers: {response.metadata.get('influencers', [])}")

        for tweet in response.data[:5]:
            tweet_dict = tweet.to_dict()
            content = tweet_dict['content'][:70] + "..." if len(tweet_dict['content']) > 70 else tweet_dict['content']
            print(f"\n   {tweet_dict['rank']}. @{tweet_dict['author']['username']}")
            print(f"      {content}")
            print(f"      ❤️ {tweet_dict['stats']['likes']} | 🔁 {tweet_dict['stats']['retweets']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Twitter Indie Hackers Tests Completed!")
    print("=" * 60)


async def test_twitter_user_profile():
    """Test fetching user profile."""
    print("\n" + "=" * 60)
    print("Testing Twitter/X User Profile Fetcher")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    # Test: Fetch profile of @levelsio
    print("\nTest: Fetch profile of @levelsio")
    print("-" * 60)

    response = await fetcher.fetch_user_profile(
        username="levelsio",
        use_cache=False,
    )

    if response.success and response.data:
        user = response.data[0]
        user_dict = user.to_dict()
        print(f"   ✓ Success: Fetched profile")
        print(f"\n   Username: @{user_dict['username']}")
        print(f"   Display Name: {user_dict['display_name']}")
        print(f"   Bio: {user_dict['bio'][:100]}..." if len(user_dict['bio']) > 100 else f"   Bio: {user_dict['bio']}")
        print(f"   Followers: {user_dict['stats']['followers']:,}")
        print(f"   Following: {user_dict['stats']['following']:,}")
        print(f"   Tweets: {user_dict['stats']['tweets']:,}")
        if user_dict['location']:
            print(f"   Location: {user_dict['location']}")
        if user_dict['website']:
            print(f"   Website: {user_dict['website']}")
    else:
        print(f"   ✗ Failed: {response.error}")

    print("\n" + "=" * 60)
    print("Twitter User Profile Tests Completed!")
    print("=" * 60)


async def test_nitter_instance_fallback():
    """Test Nitter instance fallback mechanism."""
    print("\n" + "=" * 60)
    print("Testing Nitter Instance Fallback")
    print("=" * 60)

    cache = SimpleCache()
    fetcher = TwitterFetcher(cache=cache)

    print("\nTest: Check available Nitter instances")
    print("-" * 60)
    print(f"   Configured instances: {len(fetcher.NITTER_INSTANCES)}")
    for i, instance in enumerate(fetcher.NITTER_INSTANCES, 1):
        print(f"   {i}. {instance}")

    # Try to get a working instance
    print("\n   Finding working instance...")
    instance = await fetcher._get_working_instance()
    if instance:
        print(f"   ✓ Working instance found: {instance}")
    else:
        print("   ✗ No working instance available")
        print("   Note: All Nitter instances may be temporarily down")

    print("\n" + "=" * 60)
    print("Nitter Instance Tests Completed!")
    print("=" * 60)


async def main():
    """Run all Twitter tests."""
    setup_logger()

    # Run tests
    await test_nitter_instance_fallback()
    await test_twitter_hashtag()
    await test_twitter_user_tweets()
    await test_twitter_tech_tweets()
    await test_twitter_indie_hackers()
    await test_twitter_user_profile()

    print("\n" + "=" * 80)
    print("✅ ALL TWITTER/X TESTS COMPLETED!")
    print("=" * 80)
    print("\nNote: Some tests may fail if Nitter instances are temporarily unavailable.")
    print("This is expected behavior - the fetcher will automatically try fallback instances.")


if __name__ == "__main__":
    asyncio.run(main())


"""Twitter/X fetcher implementation using Nitter instances.

Twitter/X data is fetched through Nitter, an open-source Twitter frontend.
This approach doesn't require API keys and is completely free.

Note:
- Only public tweets can be fetched
- Nitter instances may be unstable, so we use multiple fallback instances
- Rate limiting may apply depending on the instance
"""

import re
from datetime import datetime

from bs4 import BeautifulSoup

from ...models import TrendingResponse
from ...models.twitter import Tweet, TwitterUser
from ...utils import logger
from ..base import BaseFetcher


class TwitterFetcher(BaseFetcher):
    """Fetcher for Twitter/X data using Nitter instances."""

    # List of public Nitter instances (ordered by reliability)
    NITTER_INSTANCES = [
        "https://nitter.poast.org",
        "https://nitter.privacydev.net",
        "https://nitter.woodland.cafe",
        "https://nitter.lucabased.xyz",
        "https://nitter.1d4.us",
    ]

    # Popular tech hashtags for indie hackers and developers
    TECH_HASHTAGS = [
        "buildinpublic",
        "indiehackers",
        "saas",
        "startup",
        "webdev",
        "javascript",
        "python",
        "ai",
        "machinelearning",
        "opensource",
    ]

    # Popular tech influencers/indie hackers
    TECH_INFLUENCERS = [
        ("levelsio", "Pieter Levels"),  # Nomad List, Remote OK creator
        ("marc_louvion", "Marc Lou"),  # ShipFast creator
        ("dannypostmaa", "Danny Postma"),  # HeadshotPro creator
        ("taborsky_", "Tony Dinh"),  # Indie hacker
        ("dagobert_renouf", "Dagobert Renouf"),  # Logology creator
        ("araboricua", "Arvid Kahl"),  # The Bootstrapped Founder
    ]

    def __init__(self, **kwargs):
        """Initialize Twitter fetcher."""
        super().__init__(**kwargs)
        self.working_instance = None

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "twitter"

    async def _get_working_instance(self) -> str | None:
        """Find a working Nitter instance."""
        if self.working_instance:
            return self.working_instance

        for instance in self.NITTER_INSTANCES:
            try:
                response = await self.http_client.get(
                    instance,
                    timeout=5.0,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"},
                )
                if response.status_code == 200:
                    self.working_instance = instance
                    logger.info(f"Using Nitter instance: {instance}")
                    return instance
            except Exception as e:
                logger.debug(f"Nitter instance {instance} failed: {e}")
                continue

        return None

    async def fetch_hashtag_tweets(
        self,
        hashtag: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch tweets by hashtag.

        Args:
            hashtag: Hashtag to search (without #)
            limit: Number of tweets to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with tweets for the hashtag
        """
        # Clean hashtag (remove # if present)
        hashtag = hashtag.lstrip("#").lower()

        return await self.fetch_with_cache(
            data_type=f"hashtag_{hashtag}",
            fetch_func=self._fetch_hashtag_internal,
            use_cache=use_cache,
            hashtag=hashtag,
            limit=min(limit, 50),
        )

    async def _fetch_hashtag_internal(
        self, hashtag: str, limit: int = 20
    ) -> TrendingResponse:
        """Internal implementation to fetch tweets by hashtag."""
        try:
            instance = await self._get_working_instance()
            if not instance:
                return self._create_response(
                    success=False,
                    data_type=f"hashtag_{hashtag}",
                    data=[],
                    error="No working Nitter instance available",
                )

            url = f"{instance}/search?f=tweets&q=%23{hashtag}"
            logger.info(f"Fetching Twitter hashtag #{hashtag} from {url}")

            response = await self.http_client.get(
                url,
                timeout=15.0,
                headers={"User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"},
            )

            if response.status_code != 200:
                # Try next instance
                self.working_instance = None
                return self._create_response(
                    success=False,
                    data_type=f"hashtag_{hashtag}",
                    data=[],
                    error=f"Failed to fetch: HTTP {response.status_code}",
                )

            tweets = self._parse_tweets(response.text, limit, instance)

            return self._create_response(
                success=True,
                data_type=f"hashtag_{hashtag}",
                data=tweets,
                metadata={
                    "hashtag": hashtag,
                    "total_count": len(tweets),
                    "limit": limit,
                    "source": "nitter",
                    "instance": instance,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Twitter hashtag #{hashtag}: {e}")
            self.working_instance = None
            return self._create_response(
                success=False,
                data_type=f"hashtag_{hashtag}",
                data=[],
                error=str(e),
            )

    async def fetch_user_tweets(
        self,
        username: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch tweets from a specific user.

        Args:
            username: Twitter username (without @)
            limit: Number of tweets to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with user's tweets
        """
        # Clean username (remove @ if present)
        username = username.lstrip("@").lower()

        return await self.fetch_with_cache(
            data_type=f"user_{username}",
            fetch_func=self._fetch_user_tweets_internal,
            use_cache=use_cache,
            username=username,
            limit=min(limit, 50),
        )

    async def _fetch_user_tweets_internal(
        self, username: str, limit: int = 20
    ) -> TrendingResponse:
        """Internal implementation to fetch user tweets."""
        try:
            instance = await self._get_working_instance()
            if not instance:
                return self._create_response(
                    success=False,
                    data_type=f"user_{username}",
                    data=[],
                    error="No working Nitter instance available",
                )

            url = f"{instance}/{username}"
            logger.info(f"Fetching Twitter user @{username} from {url}")

            response = await self.http_client.get(
                url,
                timeout=15.0,
                headers={"User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"},
            )

            if response.status_code != 200:
                self.working_instance = None
                return self._create_response(
                    success=False,
                    data_type=f"user_{username}",
                    data=[],
                    error=f"Failed to fetch: HTTP {response.status_code}",
                )

            tweets = self._parse_tweets(response.text, limit, instance)

            return self._create_response(
                success=True,
                data_type=f"user_{username}",
                data=tweets,
                metadata={
                    "username": username,
                    "total_count": len(tweets),
                    "limit": limit,
                    "source": "nitter",
                    "instance": instance,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Twitter user @{username}: {e}")
            self.working_instance = None
            return self._create_response(
                success=False,
                data_type=f"user_{username}",
                data=[],
                error=str(e),
            )

    async def fetch_tech_tweets(
        self,
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch trending tech tweets from popular hashtags.

        This aggregates tweets from multiple tech-related hashtags:
        #buildinpublic, #indiehackers, #saas, #startup, etc.

        Args:
            limit: Total number of tweets to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with tech-related tweets
        """
        return await self.fetch_with_cache(
            data_type="tech_tweets",
            fetch_func=self._fetch_tech_tweets_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_tech_tweets_internal(self, limit: int = 30) -> TrendingResponse:
        """Internal implementation to fetch tech tweets."""
        try:
            instance = await self._get_working_instance()
            if not instance:
                return self._create_response(
                    success=False,
                    data_type="tech_tweets",
                    data=[],
                    error="No working Nitter instance available",
                )

            all_tweets = []
            tweets_per_hashtag = max(5, limit // len(self.TECH_HASHTAGS[:5]))

            # Fetch from top 5 hashtags
            for hashtag in self.TECH_HASHTAGS[:5]:
                try:
                    url = f"{instance}/search?f=tweets&q=%23{hashtag}"
                    response = await self.http_client.get(
                        url,
                        timeout=10.0,
                        headers={
                            "User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"
                        },
                    )

                    if response.status_code == 200:
                        tweets = self._parse_tweets(
                            response.text, tweets_per_hashtag, instance
                        )
                        for tweet in tweets:
                            if hashtag not in tweet.hashtags:
                                tweet.hashtags.append(hashtag)
                        all_tweets.extend(tweets)

                except Exception as e:
                    logger.warning(f"Error fetching #{hashtag}: {e}")
                    continue

            # Remove duplicates by tweet ID
            seen_ids = set()
            unique_tweets = []
            for tweet in all_tweets:
                if tweet.id not in seen_ids:
                    seen_ids.add(tweet.id)
                    unique_tweets.append(tweet)

            # Sort by engagement (likes + retweets) and limit
            unique_tweets.sort(key=lambda t: t.likes + t.retweets, reverse=True)
            unique_tweets = unique_tweets[:limit]

            # Re-rank
            for i, tweet in enumerate(unique_tweets):
                tweet.rank = i + 1

            return self._create_response(
                success=True,
                data_type="tech_tweets",
                data=unique_tweets,
                metadata={
                    "total_count": len(unique_tweets),
                    "limit": limit,
                    "hashtags_searched": self.TECH_HASHTAGS[:5],
                    "source": "nitter",
                    "instance": instance,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching tech tweets: {e}")
            return self._create_response(
                success=False,
                data_type="tech_tweets",
                data=[],
                error=str(e),
            )

    async def fetch_indie_hackers_tweets(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch tweets from popular indie hackers/tech influencers.

        Args:
            limit: Number of tweets to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with indie hacker tweets
        """
        return await self.fetch_with_cache(
            data_type="indie_hackers_tweets",
            fetch_func=self._fetch_indie_hackers_internal,
            use_cache=use_cache,
            limit=limit,
        )

    async def _fetch_indie_hackers_internal(self, limit: int = 20) -> TrendingResponse:
        """Internal implementation to fetch indie hacker tweets."""
        try:
            instance = await self._get_working_instance()
            if not instance:
                return self._create_response(
                    success=False,
                    data_type="indie_hackers_tweets",
                    data=[],
                    error="No working Nitter instance available",
                )

            all_tweets = []
            tweets_per_user = max(3, limit // len(self.TECH_INFLUENCERS))

            for username, display_name in self.TECH_INFLUENCERS:
                try:
                    url = f"{instance}/{username}"
                    response = await self.http_client.get(
                        url,
                        timeout=10.0,
                        headers={
                            "User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"
                        },
                    )

                    if response.status_code == 200:
                        tweets = self._parse_tweets(
                            response.text, tweets_per_user, instance
                        )
                        all_tweets.extend(tweets)

                except Exception as e:
                    logger.warning(f"Error fetching @{username}: {e}")
                    continue

            # Sort by engagement and limit
            all_tweets.sort(key=lambda t: t.likes + t.retweets, reverse=True)
            all_tweets = all_tweets[:limit]

            # Re-rank
            for i, tweet in enumerate(all_tweets):
                tweet.rank = i + 1

            return self._create_response(
                success=True,
                data_type="indie_hackers_tweets",
                data=all_tweets,
                metadata={
                    "total_count": len(all_tweets),
                    "limit": limit,
                    "influencers": [u for u, _ in self.TECH_INFLUENCERS],
                    "source": "nitter",
                    "instance": instance,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching indie hacker tweets: {e}")
            return self._create_response(
                success=False,
                data_type="indie_hackers_tweets",
                data=[],
                error=str(e),
            )

    async def fetch_user_profile(
        self,
        username: str,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch a Twitter user's profile information.

        Args:
            username: Twitter username (without @)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with user profile
        """
        username = username.lstrip("@").lower()

        return await self.fetch_with_cache(
            data_type=f"profile_{username}",
            fetch_func=self._fetch_user_profile_internal,
            use_cache=use_cache,
            username=username,
        )

    async def _fetch_user_profile_internal(self, username: str) -> TrendingResponse:
        """Internal implementation to fetch user profile."""
        try:
            instance = await self._get_working_instance()
            if not instance:
                return self._create_response(
                    success=False,
                    data_type=f"profile_{username}",
                    data=[],
                    error="No working Nitter instance available",
                )

            url = f"{instance}/{username}"
            logger.info(f"Fetching Twitter profile @{username} from {url}")

            response = await self.http_client.get(
                url,
                timeout=15.0,
                headers={"User-Agent": "Mozilla/5.0 (compatible; TrendingBot/1.0)"},
            )

            if response.status_code != 200:
                self.working_instance = None
                return self._create_response(
                    success=False,
                    data_type=f"profile_{username}",
                    data=[],
                    error=f"Failed to fetch: HTTP {response.status_code}",
                )

            user = self._parse_user_profile(response.text, username, instance)

            if user:
                return self._create_response(
                    success=True,
                    data_type=f"profile_{username}",
                    data=[user],
                    metadata={
                        "username": username,
                        "source": "nitter",
                        "instance": instance,
                    },
                )
            else:
                return self._create_response(
                    success=False,
                    data_type=f"profile_{username}",
                    data=[],
                    error="Could not parse user profile",
                )

        except Exception as e:
            logger.error(f"Error fetching Twitter profile @{username}: {e}")
            return self._create_response(
                success=False,
                data_type=f"profile_{username}",
                data=[],
                error=str(e),
            )

    def _parse_tweets(self, html: str, limit: int, instance: str) -> list[Tweet]:
        """Parse tweets from Nitter HTML."""
        tweets = []
        soup = BeautifulSoup(html, "html.parser")

        # Find all tweet items
        tweet_items = soup.select(".timeline-item")

        for i, item in enumerate(tweet_items[:limit]):
            try:
                # Skip pinned tweets indicator
                if item.select_one(".pinned"):
                    continue

                # Get tweet content
                content_elem = item.select_one(".tweet-content")
                content = content_elem.get_text(strip=True) if content_elem else ""

                # Get author info
                username_elem = item.select_one(".username")
                username = (
                    username_elem.get_text(strip=True).lstrip("@")
                    if username_elem
                    else ""
                )

                fullname_elem = item.select_one(".fullname")
                display_name = (
                    fullname_elem.get_text(strip=True) if fullname_elem else username
                )

                # Get tweet link/ID
                tweet_link = item.select_one(".tweet-link")
                tweet_url = ""
                tweet_id = ""
                if tweet_link:
                    href = tweet_link.get("href", "")
                    tweet_url = f"https://twitter.com{href.replace('#m', '')}"
                    # Extract ID from URL like /username/status/123456789
                    match = re.search(r"/status/(\d+)", href)
                    if match:
                        tweet_id = match.group(1)

                # Get date
                date_elem = item.select_one(".tweet-date a")
                created_at = None
                if date_elem:
                    date_str = date_elem.get("title", "")
                    try:
                        # Parse format like "Dec 1, 2025 · 10:30 AM UTC"
                        created_at = datetime.strptime(
                            date_str.split(" · ")[0], "%b %d, %Y"
                        )
                    except (ValueError, IndexError):
                        pass

                # Get stats
                stats = self._parse_tweet_stats(item)

                # Extract hashtags from content
                hashtags = re.findall(r"#(\w+)", content)

                # Extract mentions from content
                mentions = re.findall(r"@(\w+)", content)

                # Check if retweet or quote
                is_retweet = bool(item.select_one(".retweet-header"))
                is_quote = bool(item.select_one(".quote"))

                if tweet_id and content:
                    tweet = Tweet(
                        rank=len(tweets) + 1,
                        id=tweet_id,
                        content=content,
                        author_username=username,
                        author_display_name=display_name,
                        created_at=created_at,
                        url=tweet_url,
                        replies=stats.get("replies", 0),
                        retweets=stats.get("retweets", 0),
                        likes=stats.get("likes", 0),
                        quotes=stats.get("quotes", 0),
                        is_retweet=is_retweet,
                        is_quote=is_quote,
                        hashtags=hashtags,
                        mentions=mentions,
                    )
                    tweets.append(tweet)

            except Exception as e:
                logger.warning(f"Error parsing tweet: {e}")
                continue

        return tweets

    def _parse_tweet_stats(self, item) -> dict:
        """Parse tweet statistics from HTML element."""
        stats = {"replies": 0, "retweets": 0, "likes": 0, "quotes": 0}

        stat_container = item.select_one(".tweet-stat")
        if not stat_container:
            # Try alternative selector
            stat_container = item

        # Parse each stat
        for stat_elem in stat_container.select(".icon-container"):
            text = stat_elem.get_text(strip=True)
            # Remove commas from numbers
            num_str = re.sub(r"[^\d]", "", text) or "0"
            try:
                num = int(num_str)
            except ValueError:
                num = 0

            # Determine stat type by icon class
            if stat_elem.select_one(".icon-comment"):
                stats["replies"] = num
            elif stat_elem.select_one(".icon-retweet"):
                stats["retweets"] = num
            elif stat_elem.select_one(".icon-heart"):
                stats["likes"] = num
            elif stat_elem.select_one(".icon-quote"):
                stats["quotes"] = num

        return stats

    def _parse_user_profile(
        self, html: str, username: str, instance: str
    ) -> TwitterUser | None:
        """Parse user profile from Nitter HTML."""
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Get profile header
            profile = soup.select_one(".profile-card")
            if not profile:
                return None

            # Get display name
            fullname_elem = profile.select_one(".profile-card-fullname")
            display_name = (
                fullname_elem.get_text(strip=True) if fullname_elem else username
            )

            # Get bio
            bio_elem = profile.select_one(".profile-bio")
            bio = bio_elem.get_text(strip=True) if bio_elem else ""

            # Get stats
            stats = {}
            for stat_elem in profile.select(".profile-stat"):
                label = stat_elem.select_one(".profile-stat-header")
                value = stat_elem.select_one(".profile-stat-num")
                if label and value:
                    label_text = label.get_text(strip=True).lower()
                    value_text = value.get_text(strip=True).replace(",", "")
                    try:
                        stats[label_text] = int(value_text)
                    except ValueError:
                        stats[label_text] = 0

            # Get location
            location_elem = profile.select_one(".profile-location")
            location = location_elem.get_text(strip=True) if location_elem else ""

            # Get website
            website_elem = profile.select_one(".profile-website a")
            website = website_elem.get("href", "") if website_elem else ""

            # Get join date
            join_elem = profile.select_one(".profile-joindate")
            joined_date = join_elem.get_text(strip=True) if join_elem else ""

            return TwitterUser(
                username=username,
                display_name=display_name,
                bio=bio,
                url=f"https://twitter.com/{username}",
                followers=stats.get("followers", 0),
                following=stats.get("following", 0),
                tweets_count=stats.get("tweets", 0),
                joined_date=joined_date,
                location=location,
                website=website,
                verified=bool(profile.select_one(".verified-icon")),
            )

        except Exception as e:
            logger.error(f"Error parsing user profile: {e}")
            return None


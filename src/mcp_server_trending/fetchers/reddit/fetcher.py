"""Reddit fetcher implementation using PRAW (Python Reddit API Wrapper)."""

import os
from datetime import datetime

from ...models import RedditPost, TrendingResponse
from ...utils import logger
from ..base import BaseFetcher


class RedditFetcher(BaseFetcher):
    """Fetcher for Reddit trending posts using PRAW."""

    # Popular subreddits for indie developers
    INDIE_SUBREDDITS = {
        "sideproject": "r/SideProject",
        "entrepreneur": "r/Entrepreneur",
        "startups": "r/startups",
        "saas": "r/SaaS",
        "webdev": "r/webdev",
        "programming": "r/programming",
        "indiebiz": "r/EntrepreneurRideAlong",
    }

    # Topic to subreddits mapping for intelligent querying
    TOPIC_SUBREDDITS = {
        "ai": [
            "MachineLearning",
            "artificial",
            "ChatGPT",
            "OpenAI",
            "StableDiffusion",
            "LocalLLaMA",
            "Claude",
            "Gemini",
            "Grok",
            "Perplexity",
            "Bing",
            "Google",
        ],
        "ml": ["MachineLearning", "learnmachinelearning", "datascience", "deeplearning"],
        "crypto": ["cryptocurrency", "Bitcoin", "ethereum", "CryptoMarkets", "CryptoTechnology"],
        "blockchain": ["blockchain", "ethereum", "Bitcoin", "CryptoCurrency"],
        "indie": ["SideProject", "Entrepreneur", "EntrepreneurRideAlong", "indiebiz", "startups"],
        "startup": ["startups", "Entrepreneur", "smallbusiness", "SideProject"],
        "saas": ["SaaS", "microSaaS", "startups", "Entrepreneur"],
        "programming": [
            "programming",
            "learnprogramming",
            "webdev",
            "coding",
            "Python",
            "javascript",
            "typescript",
            "rust",
            "go",
            "swift",
            "java",
        ],
        "python": ["Python", "learnpython", "pythonforengineers", "django", "flask"],
        "javascript": ["javascript", "learnjavascript", "node", "reactjs", "vuejs"],
        "web": ["webdev", "web_design", "Frontend", "Backend", "reactjs"],
        "mobile": ["androiddev", "iOSProgramming", "reactnative", "FlutterDev"],
        "design": ["web_design", "UI_Design", "UXDesign", "graphic_design"],
        "business": ["Entrepreneur", "smallbusiness", "business", "marketing"],
        "marketing": ["marketing", "digital_marketing", "SEO", "content_marketing"],
        "freelance": ["freelance", "forhire", "digitalnomad", "WorkOnline"],
        "remote": ["digitalnomad", "RemoteJobs", "WorkOnline", "remotework"],
        "gaming": ["gaming", "gamedev", "IndieGaming", "Unity3D", "unrealengine"],
        "iot": ["IOT", "homeautomation", "raspberry_pi", "arduino"],
        "devops": ["devops", "kubernetes", "docker", "aws", "cloudcomputing"],
        "security": ["netsec", "cybersecurity", "AskNetsec", "hacking"],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://www.reddit.com"

        # Reddit API credentials (optional)
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit = None

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "reddit"

    def _get_reddit_client(self):
        """Get or create PRAW Reddit client."""
        if self.reddit is not None:
            return self.reddit

        import praw

        # Check if credentials are configured
        if self.client_id and self.client_secret:
            logger.info("Initializing PRAW with OAuth credentials")
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent="mcp-server-trending/1.0 by indie_developers",
            )
        else:
            logger.info("Reddit OAuth credentials not configured - using read-only mode")
            # Try read-only mode without credentials
            self.reddit = praw.Reddit(
                client_id="",
                client_secret="",
                user_agent="mcp-server-trending/1.0 by indie_developers",
                check_for_async=False,
            )

        return self.reddit

    async def fetch_subreddit_hot(
        self,
        subreddit: str,
        time_range: str = "day",
        limit: int = 25,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch hot posts from a subreddit.

        Args:
            subreddit: Subreddit name (without r/)
            time_range: Time range for posts ('hour', 'day', 'week', 'month', 'year', 'all')
            limit: Number of posts to fetch (1-100, default: 25)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with hot posts
        """
        return await self.fetch_with_cache(
            data_type="subreddit_hot",
            fetch_func=self._fetch_subreddit_hot_internal,
            use_cache=use_cache,
            subreddit=subreddit,
            time_range=time_range,
            limit=min(limit, 100),
        )

    async def _fetch_subreddit_hot_internal(
        self, subreddit: str, time_range: str = "day", limit: int = 25
    ) -> TrendingResponse:
        """Internal implementation to fetch hot posts using PRAW."""
        try:
            reddit = self._get_reddit_client()
            subreddit_obj = reddit.subreddit(subreddit)

            logger.info(f"Fetching hot posts from r/{subreddit} using PRAW (limit={limit})")

            # Get hot posts
            posts_data = []
            for submission in subreddit_obj.hot(limit=limit):
                post = RedditPost(
                    rank=len(posts_data) + 1,
                    id=submission.id,
                    title=submission.title,
                    url=submission.url,
                    permalink=f"{self.base_url}{submission.permalink}",
                    author=submission.author.name if submission.author else "[deleted]",
                    subreddit=subreddit,
                    subreddit_url=f"{self.base_url}/r/{subreddit}",
                    score=submission.score,
                    upvote_ratio=submission.upvote_ratio,
                    num_comments=submission.num_comments,
                    created_at=datetime.fromtimestamp(submission.created_utc),
                    is_self=submission.is_self,
                    selftext=submission.selftext[:500] if submission.selftext else "",
                    domain=submission.domain,
                    flair=submission.link_flair_text,
                    is_video=submission.is_video,
                    thumbnail_url=submission.thumbnail
                    if submission.thumbnail.startswith("http")
                    else None,
                    distinguished=submission.distinguished,
                    stickied=submission.stickied,
                    over_18=submission.over_18,
                )
                posts_data.append(post)

            return self._create_response(
                success=True,
                data_type="subreddit_hot",
                data=posts_data,
                metadata={
                    "subreddit": subreddit,
                    "time_range": time_range,
                    "total_count": len(posts_data),
                    "limit": limit,
                    "method": "praw",
                },
            )

        except Exception as e:
            logger.warning(f"Error fetching Reddit hot posts from r/{subreddit}: {e}")
            logger.info("Returning placeholder data with Reddit link")

            # Return placeholder data as fallback
            posts = []
            for i in range(min(limit, 5)):
                posts.append(
                    RedditPost(
                        rank=i + 1,
                        id=f"placeholder-{i + 1}",
                        title=f"Visit Reddit to see r/{subreddit} hot posts",
                        url=f"{self.base_url}/r/{subreddit}/hot",
                        permalink=f"{self.base_url}/r/{subreddit}/hot",
                        author="reddit",
                        subreddit=subreddit,
                        subreddit_url=f"{self.base_url}/r/{subreddit}",
                        score=0,
                        upvote_ratio=0.0,
                        num_comments=0,
                        created_at=datetime.now(),
                        is_self=False,
                        selftext="",
                        domain="reddit.com",
                        flair=None,
                        is_video=False,
                        thumbnail_url=None,
                        distinguished=None,
                        stickied=False,
                        over_18=False,
                    )
                )

            return self._create_response(
                success=True,
                data_type="subreddit_hot",
                data=posts,
                metadata={
                    "subreddit": subreddit,
                    "time_range": time_range,
                    "total_count": len(posts),
                    "limit": limit,
                    "note": f"Reddit API requires authentication. Configure REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to get real data. Visit https://www.reddit.com/r/{subreddit} to browse posts.",
                    "error": str(e),
                },
            )

    async def fetch_subreddit_top(
        self,
        subreddit: str,
        time_range: str = "week",
        limit: int = 25,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch top posts from a subreddit.

        Args:
            subreddit: Subreddit name (without r/)
            time_range: Time range for top posts ('hour', 'day', 'week', 'month', 'year', 'all')
            limit: Number of posts to fetch (1-100, default: 25)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with top posts
        """
        return await self.fetch_with_cache(
            data_type="subreddit_top",
            fetch_func=self._fetch_subreddit_top_internal,
            use_cache=use_cache,
            subreddit=subreddit,
            time_range=time_range,
            limit=min(limit, 100),
        )

    async def _fetch_subreddit_top_internal(
        self, subreddit: str, time_range: str = "week", limit: int = 25
    ) -> TrendingResponse:
        """Internal implementation to fetch top posts."""
        try:
            # Try OAuth first if credentials are configured
            token = await self._get_access_token()

            if token:
                # Use OAuth API
                url = f"{self.api_url}/r/{subreddit}/top"
                params = {"limit": limit, "t": time_range}
                headers = {
                    **self.reddit_headers,
                    "Authorization": f"Bearer {token}",
                }
                logger.info(
                    f"Fetching top posts from r/{subreddit} using OAuth (time_range={time_range})"
                )
            else:
                # Fallback to public API
                url = f"{self.public_api_url}/r/{subreddit}/top.json"
                params = {"limit": limit, "t": time_range}
                headers = self.reddit_headers
                logger.info(
                    f"Fetching top posts from r/{subreddit} using public API (time_range={time_range})"
                )

            response = await self.http_client.get(url, params=params, headers=headers)
            data = response.json()

            posts = self._parse_posts(data, subreddit)

            return self._create_response(
                success=True,
                data_type="subreddit_top",
                data=posts,
                metadata={
                    "subreddit": subreddit,
                    "time_range": time_range,
                    "total_count": len(posts),
                    "limit": limit,
                    "method": "oauth" if token else "public",
                },
            )

        except Exception as e:
            # Reddit often blocks unauthenticated requests, return helpful placeholder
            logger.warning(f"Error fetching Reddit top posts from r/{subreddit}: {e}")
            logger.info("Returning placeholder data with Reddit link")

            posts = []
            for i in range(min(limit, 5)):
                posts.append(
                    RedditPost(
                        rank=i + 1,
                        id=f"placeholder-{i + 1}",
                        title=f"Visit Reddit to see r/{subreddit} top posts",
                        url=f"{self.base_url}/r/{subreddit}/top?t={time_range}",
                        permalink=f"{self.base_url}/r/{subreddit}/top?t={time_range}",
                        author="reddit",
                        subreddit=subreddit,
                        subreddit_url=f"{self.base_url}/r/{subreddit}",
                        score=0,
                        upvote_ratio=0.0,
                        num_comments=0,
                        created_at=datetime.now(),
                        is_self=False,
                        selftext="",
                        domain="reddit.com",
                        flair=None,
                        is_video=False,
                        thumbnail_url=None,
                        distinguished=None,
                        stickied=False,
                        over_18=False,
                    )
                )

            return self._create_response(
                success=True,
                data_type="subreddit_top",
                data=posts,
                metadata={
                    "subreddit": subreddit,
                    "time_range": time_range,
                    "total_count": len(posts),
                    "limit": limit,
                    "note": f"Reddit API requires authentication. Configure REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to get real data. Visit https://www.reddit.com/r/{subreddit} to browse posts.",
                    "error": str(e),
                },
            )

    async def fetch_multi_subreddits(
        self,
        subreddits: list[str],
        sort_by: str = "hot",
        time_range: str = "day",
        limit: int = 10,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch posts from multiple subreddits.

        Args:
            subreddits: List of subreddit names
            sort_by: Sort method ('hot', 'top', 'new')
            time_range: Time range for posts
            limit: Number of posts per subreddit
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with posts from all subreddits
        """
        all_posts = []

        for subreddit in subreddits:
            if sort_by == "hot":
                response = await self.fetch_subreddit_hot(subreddit, time_range, limit, use_cache)
            else:  # top
                response = await self.fetch_subreddit_top(subreddit, time_range, limit, use_cache)

            if response.success and response.data:
                all_posts.extend(response.data)

        # Sort by score
        all_posts.sort(key=lambda p: p.score if hasattr(p, "score") else 0, reverse=True)

        return self._create_response(
            success=True,
            data_type="multi_subreddits",
            data=all_posts,
            metadata={
                "subreddits": subreddits,
                "sort_by": sort_by,
                "time_range": time_range,
                "total_count": len(all_posts),
            },
        )

    async def search_subreddits(
        self,
        query: str,
        limit: int = 10,
    ) -> list[str]:
        """
        Search for subreddits by keyword using Reddit Search API.

        Args:
            query: Search keyword (e.g., 'machine learning', '区块链', 'startup')
            limit: Maximum number of subreddits to return

        Returns:
            List of subreddit names (without 'r/' prefix)
        """
        try:
            # Try OAuth first if credentials are configured
            token = await self._get_access_token()

            if token:
                # Use OAuth API
                url = f"{self.api_url}/subreddits/search"
                params = {
                    "q": query,
                    "limit": limit,
                    "sort": "relevance",
                }
                headers = {
                    **self.reddit_headers,
                    "Authorization": f"Bearer {token}",
                }
                logger.info(f"Searching subreddits with query: '{query}' using OAuth")
            else:
                # Fallback to public API
                url = f"{self.public_api_url}/subreddits/search.json"
                params = {
                    "q": query,
                    "limit": limit,
                    "sort": "relevance",
                }
                headers = self.reddit_headers
                logger.info(f"Searching subreddits with query: '{query}' using public API")

            response = await self.http_client.get(url, params=params, headers=headers)
            data = response.json()

            subreddits = []
            children = data.get("data", {}).get("children", [])

            for item in children:
                subreddit_data = item.get("data", {})
                subreddit_name = subreddit_data.get("display_name")

                # Filter out NSFW and quarantined subreddits
                if (
                    subreddit_name
                    and not subreddit_data.get("over18", False)
                    and not subreddit_data.get("quarantine", False)
                ):
                    subreddits.append(subreddit_name)

            logger.info(f"Found {len(subreddits)} subreddits for query '{query}': {subreddits[:5]}")
            return subreddits

        except Exception as e:
            logger.warning(f"Error searching subreddits for '{query}': {e}")
            return []

    async def fetch_by_topic(
        self,
        topic: str | None = None,
        sort_by: str = "hot",
        time_range: str = "day",
        limit_per_subreddit: int = 10,
        max_total: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch posts by topic. Automatically selects relevant subreddits.

        Args:
            topic: Topic keyword (e.g., 'ai', 'crypto', 'indie'). If None, uses default indie subreddits.
                   Supports ANY keyword - will search Reddit for relevant subreddits if not in predefined list.
            sort_by: Sort method ('hot', 'top')
            time_range: Time range for posts
            limit_per_subreddit: Number of posts per subreddit
            max_total: Maximum total posts to return
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with posts from topic-related subreddits
        """
        # Determine which subreddits to query
        if topic is None:
            # Use default indie subreddits
            subreddits = list(self.INDIE_SUBREDDITS.keys())
            topic_used = "indie (default)"
        else:
            # Normalize topic
            topic_normalized = topic.lower().strip()

            # Try to find matching topic
            matched_subreddits = self.TOPIC_SUBREDDITS.get(topic_normalized)

            if matched_subreddits:
                subreddits = matched_subreddits
                topic_used = topic_normalized
            else:
                # If no exact match, try partial matching
                matched_topics = [
                    (t, subs)
                    for t, subs in self.TOPIC_SUBREDDITS.items()
                    if topic_normalized in t or t in topic_normalized
                ]

                if matched_topics:
                    # Use the first match
                    topic_used, subreddits = matched_topics[0]
                else:
                    # NEW: Search Reddit for relevant subreddits using keyword
                    logger.info(
                        f"No predefined match for '{topic_normalized}', searching Reddit..."
                    )
                    searched_subreddits = await self.search_subreddits(
                        query=topic_normalized, limit=10
                    )

                    if searched_subreddits:
                        # Found subreddits via search
                        subreddits = searched_subreddits
                        topic_used = f"search: {topic_normalized}"
                        logger.info(f"Using {len(subreddits)} subreddits from search results")
                    else:
                        # Fallback: treat as subreddit name
                        subreddits = [topic_normalized]
                        topic_used = f"custom ({topic_normalized})"

        logger.info(
            f"Fetching Reddit posts for topic '{topic_used}' from subreddits: {subreddits[:5]}..."
        )

        # Fetch posts from all matched subreddits
        all_posts = []
        for subreddit in subreddits[:10]:  # Limit to 10 subreddits to avoid too many requests
            try:
                if sort_by == "hot":
                    response = await self.fetch_subreddit_hot(
                        subreddit, time_range, limit_per_subreddit, use_cache
                    )
                else:  # top
                    response = await self.fetch_subreddit_top(
                        subreddit, time_range, limit_per_subreddit, use_cache
                    )

                if response.success and response.data:
                    all_posts.extend(response.data)
            except Exception as e:
                logger.warning(f"Error fetching from r/{subreddit}: {e}")
                continue

        # Sort by score and limit
        all_posts.sort(key=lambda p: p.score if hasattr(p, "score") else 0, reverse=True)
        all_posts = all_posts[:max_total]

        return self._create_response(
            success=True,
            data_type="topic_trending",
            data=all_posts,
            metadata={
                "topic": topic_used,
                "subreddits_queried": subreddits[:10],
                "sort_by": sort_by,
                "time_range": time_range,
                "total_count": len(all_posts),
            },
        )

    def _parse_posts(self, data: dict, subreddit: str) -> list[RedditPost]:
        """Parse posts from Reddit API response."""
        posts = []
        rank = 1

        try:
            children = data.get("data", {}).get("children", [])

            for item in children:
                try:
                    post_data = item.get("data", {})

                    post = RedditPost(
                        rank=rank,
                        id=post_data.get("id", ""),
                        title=post_data.get("title", ""),
                        url=post_data.get("url", ""),
                        permalink=f"{self.base_url}{post_data.get('permalink', '')}",
                        author=post_data.get("author", "[deleted]"),
                        subreddit=subreddit,
                        subreddit_url=f"{self.base_url}/r/{subreddit}",
                        score=post_data.get("score", 0),
                        upvote_ratio=post_data.get("upvote_ratio", 0.0),
                        num_comments=post_data.get("num_comments", 0),
                        created_at=datetime.fromtimestamp(post_data.get("created_utc", 0)),
                        is_self=post_data.get("is_self", False),
                        selftext=post_data.get("selftext", "")[:500],  # Limit to 500 chars
                        domain=post_data.get("domain", ""),
                        flair=post_data.get("link_flair_text"),
                        is_video=post_data.get("is_video", False),
                        thumbnail_url=post_data.get("thumbnail")
                        if post_data.get("thumbnail", "").startswith("http")
                        else None,
                        distinguished=post_data.get("distinguished"),
                        stickied=post_data.get("stickied", False),
                        over_18=post_data.get("over_18", False),
                    )

                    posts.append(post)
                    rank += 1

                except Exception as e:
                    logger.warning(f"Error parsing Reddit post: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing Reddit response: {e}")

        return posts

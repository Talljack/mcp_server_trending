"""Product Hunt fetcher implementation using official GraphQL API."""

import os
from datetime import datetime

from ...models.base import TrendingResponse
from ...models.producthunt import ProductHuntProduct
from ...utils import logger
from ..base import BaseFetcher


class ProductHuntFetcher(BaseFetcher):
    """
    Fetcher for Product Hunt data using official GraphQL API.

    Requires:
    - PRODUCTHUNT_CLIENT_ID: Your Product Hunt app's Client ID
    - PRODUCTHUNT_CLIENT_SECRET: Your Product Hunt app's Client Secret

    Get credentials from: https://www.producthunt.com/v2/oauth/applications
    """

    BASE_URL = "https://www.producthunt.com"
    API_URL = "https://api.producthunt.com/v2/api/graphql"
    TOKEN_URL = "https://api.producthunt.com/v2/oauth/token"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = os.getenv("PRODUCTHUNT_CLIENT_ID")
        self.client_secret = os.getenv("PRODUCTHUNT_CLIENT_SECRET")
        self._access_token = None  # Cached access token

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "producthunt"

    async def _get_access_token(self) -> str | None:
        """
        Get access token using Client Credentials flow.

        Returns:
            Access token or None if credentials not configured
        """
        # Return cached token if available
        if self._access_token:
            return self._access_token

        # Check if credentials are configured
        if not self.client_id or not self.client_secret:
            logger.warning("Product Hunt credentials not configured")
            return None

        try:
            logger.info("Fetching Product Hunt access token using Client Credentials")

            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            }

            response = await self.http_client.post(
                self.TOKEN_URL,
                json=token_data,
                headers={"Content-Type": "application/json"},
            )

            data = response.json()
            self._access_token = data.get("access_token")

            if self._access_token:
                logger.info("Successfully obtained Product Hunt access token")
                return self._access_token
            else:
                logger.error("No access_token in Product Hunt OAuth response")
                return None

        except Exception as e:
            logger.error(f"Error fetching Product Hunt access token: {e}")
            return None

    async def fetch_products(
        self,
        time_range: str = "today",
        topic: str | None = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch Product Hunt products using GraphQL API.

        Args:
            time_range: Time range (today, week, month)
            topic: Optional topic filter
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with product data
        """
        return await self.fetch_with_cache(
            data_type=f"products_{time_range}",
            fetch_func=self._fetch_products_internal,
            use_cache=use_cache,
            time_range=time_range,
            topic=topic,
        )

    async def _fetch_products_internal(
        self,
        time_range: str = "today",
        topic: str | None = None,
    ) -> TrendingResponse:
        """Internal method to fetch products via GraphQL API."""
        try:
            # Get access token
            access_token = await self._get_access_token()

            if not access_token:
                logger.warning("Product Hunt API credentials not configured")
                return self._create_response(
                    success=True,
                    data_type=f"products_{time_range}",
                    data=self._get_fallback_products(),
                    metadata={
                        "total_count": 5,
                        "time_range": time_range,
                        "source": "placeholder",
                        "note": "Product Hunt API credentials not configured. Set PRODUCTHUNT_CLIENT_ID and PRODUCTHUNT_CLIENT_SECRET environment variables. Get credentials from: https://www.producthunt.com/v2/oauth/applications",
                    },
                )

            # Build GraphQL query
            query = self._build_graphql_query(time_range, topic)

            # Set authorization header
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Make GraphQL request
            logger.info(f"Fetching Product Hunt products via API (time_range={time_range})")
            response = await self.http_client.post(
                self.API_URL,
                json={"query": query},
                headers=headers,
            )

            data = response.json()

            # Check for GraphQL errors
            if "errors" in data:
                error_msg = data["errors"][0].get("message", "Unknown GraphQL error")
                logger.error(f"Product Hunt API error: {error_msg}")
                return self._create_response(
                    success=False,
                    data_type=f"products_{time_range}",
                    data=[],
                    error=error_msg,
                )

            # Extract products from response
            products = self._parse_graphql_response(data)

            # Filter by topic if specified
            if topic:
                products = [
                    p for p in products if any(topic.lower() in t.lower() for t in p.topics)
                ]

            logger.info(f"Successfully fetched {len(products)} products from Product Hunt API")

            metadata = {
                "total_count": len(products),
                "time_range": time_range,
                "topic": topic,
                "source": "graphql_api",
            }

            return self._create_response(
                success=True,
                data_type=f"products_{time_range}",
                data=products,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching Product Hunt products: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type=f"products_{time_range}",
                data=[],
                error=str(e),
            )

    def _build_graphql_query(self, time_range: str = "today", topic: str | None = None) -> str:
        """
        Build GraphQL query for fetching products.

        Args:
            time_range: Time range filter
            topic: Optional topic filter

        Returns:
            GraphQL query string
        """
        # Determine ordering based on time range
        order_map = {
            "today": "RANKING",
            "week": "VOTES",
            "month": "VOTES",
        }
        order = order_map.get(time_range, "RANKING")

        # Build topic filter if provided
        topic_filter = f', topic: "{topic}"' if topic else ""

        # GraphQL query
        query = f"""
        {{
          posts(first: 20, order: {order}{topic_filter}) {{
            edges {{
              node {{
                id
                name
                tagline
                description
                url
                website
                votesCount
                commentsCount
                featuredAt
                thumbnail {{
                  url
                }}
                topics {{
                  edges {{
                    node {{
                      name
                    }}
                  }}
                }}
                makers {{
                  edges {{
                    node {{
                      name
                      username
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        return query

    def _parse_graphql_response(self, data: dict) -> list[ProductHuntProduct]:
        """
        Parse GraphQL response into ProductHuntProduct objects.

        Args:
            data: GraphQL response data

        Returns:
            List of ProductHuntProduct objects
        """
        products = []

        try:
            edges = data.get("data", {}).get("posts", {}).get("edges", [])

            for rank, edge in enumerate(edges, 1):
                try:
                    node = edge.get("node", {})

                    # Extract topics
                    topics = []
                    topic_edges = node.get("topics", {}).get("edges", [])
                    for topic_edge in topic_edges:
                        topic_name = topic_edge.get("node", {}).get("name")
                        if topic_name:
                            topics.append(topic_name)

                    # Extract makers
                    makers = []
                    maker_edges = node.get("makers", {}).get("edges", [])
                    for maker_edge in maker_edges:
                        maker_node = maker_edge.get("node", {})
                        maker_name = maker_node.get("name") or maker_node.get("username")
                        if maker_name:
                            makers.append(maker_name)

                    # Get thumbnail URL
                    thumbnail_url = None
                    thumbnail = node.get("thumbnail")
                    if thumbnail:
                        thumbnail_url = thumbnail.get("url")

                    # Parse featured date
                    featured_at = datetime.now()
                    if node.get("featuredAt"):
                        try:
                            # Product Hunt returns ISO 8601 format
                            featured_at = datetime.fromisoformat(
                                node["featuredAt"].replace("Z", "+00:00")
                            )
                        except Exception as e:
                            logger.warning(f"Error parsing featuredAt date: {e}")

                    product = ProductHuntProduct(
                        rank=rank,
                        name=node.get("name", "Unknown"),
                        tagline=node.get("tagline", ""),
                        description=node.get("description", ""),
                        url=node.get("url", ""),
                        product_url=node.get("website", ""),
                        votes=node.get("votesCount", 0),
                        comments_count=node.get("commentsCount", 0),
                        thumbnail=thumbnail_url,
                        topics=topics,
                        makers=makers,
                        featured_at=featured_at,
                    )

                    products.append(product)

                except Exception as e:
                    logger.warning(f"Error parsing product at rank {rank}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing GraphQL response: {e}")

        return products

    def _get_fallback_products(self) -> list[ProductHuntProduct]:
        """
        Get fallback products when API credentials not configured.

        Returns:
            List with placeholder products
        """
        logger.info("Using fallback Product Hunt data")

        placeholders = [
            ("Configure Product Hunt API", "Set PRODUCTHUNT_CLIENT_ID and PRODUCTHUNT_CLIENT_SECRET", ["Setup"]),
            ("Get Credentials", "Visit https://www.producthunt.com/v2/oauth/applications", ["API"]),
            ("Create OAuth App", "Create a new application and get Client ID/Secret", ["OAuth"]),
            ("Set Environment Variables", "Add credentials to your .env file", ["Config"]),
            ("Enjoy Real Data", "Restart server to fetch real Product Hunt data", ["Success"]),
        ]

        return [
            ProductHuntProduct(
                rank=i,
                name=name,
                tagline=tagline,
                description=f"{tagline}. Get your API credentials from Product Hunt to access real trending products.",
                url=self.BASE_URL,
                product_url="https://www.producthunt.com/v2/oauth/applications",
                votes=0,
                comments_count=0,
                topics=topics,
                makers=["Product Hunt"],
                featured_at=datetime.now(),
            )
            for i, (name, tagline, topics) in enumerate(placeholders, 1)
        ]

    async def fetch_today(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for today's products."""
        return await self.fetch_products("today", use_cache=use_cache)

    async def fetch_this_week(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this week's products."""
        return await self.fetch_products("week", use_cache=use_cache)

    async def fetch_this_month(self, use_cache: bool = True) -> TrendingResponse:
        """Convenience method for this month's products."""
        return await self.fetch_products("month", use_cache=use_cache)

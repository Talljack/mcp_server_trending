"""Gumroad fetcher implementation.

Gumroad is a popular platform for creators to sell digital products.
This fetcher scrapes the Gumroad discover page to find trending products.

Note:
- Gumroad doesn't have a public API for discover/trending
- We scrape the public discover pages
- Rate limiting may apply
"""

import re
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from ...models import TrendingResponse
from ...models.gumroad import GumroadCreator, GumroadProduct
from ...utils import logger
from ..base import BaseFetcher


class GumroadFetcher(BaseFetcher):
    """Fetcher for Gumroad products and creators."""

    BASE_URL = "https://gumroad.com"
    DISCOVER_URL = "https://gumroad.com/discover"

    # Popular categories on Gumroad
    CATEGORIES = [
        "3d",
        "audio",
        "business",
        "comics",
        "design",
        "drawing-and-painting",
        "education",
        "fiction-books",
        "films",
        "fitness-and-health",
        "fonts",
        "games",
        "music",
        "nonfiction-books",
        "other",
        "photography",
        "programming",
        "self-improvement",
        "software",
        "writing",
    ]

    def __init__(self, **kwargs):
        """Initialize Gumroad fetcher."""
        super().__init__(**kwargs)

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "gumroad"

    async def fetch_discover_products(
        self,
        category: str | None = None,
        sort: str = "featured",
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch products from Gumroad discover page.

        Args:
            category: Product category (e.g., 'programming', 'design', 'software')
            sort: Sort order ('featured', 'newest', 'popular')
            limit: Number of products to fetch (max 50)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with Gumroad products
        """
        cache_key = f"discover_{category or 'all'}_{sort}"

        return await self.fetch_with_cache(
            data_type=cache_key,
            fetch_func=self._fetch_discover_internal,
            use_cache=use_cache,
            category=category,
            sort=sort,
            limit=min(limit, 50),
        )

    async def _fetch_discover_internal(
        self,
        category: str | None = None,
        sort: str = "featured",
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch discover products."""
        try:
            # Build URL - Gumroad uses /discover with ?tags= for categories
            url = self.DISCOVER_URL
            params = []
            
            # Add category/tag filter
            if category:
                params.append(f"tags={category}")

            # Add sort parameter
            if sort == "newest":
                params.append("sort=newest")
            elif sort == "popular":
                params.append("sort=popular")
            # 'featured' is default, no param needed
            
            if params:
                url += "?" + "&".join(params)

            logger.info(f"Fetching Gumroad discover products from {url}")

            # Use httpx directly with follow_redirects for Gumroad
            import httpx
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(
                    url,
                    timeout=15.0,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    },
                )

            if response.status_code != 200:
                return self._create_response(
                    success=False,
                    data_type=f"discover_{category or 'all'}_{sort}",
                    data=[],
                    error=f"Failed to fetch: HTTP {response.status_code}",
                )

            products = self._parse_discover_page(response.text, limit, category)

            return self._create_response(
                success=True,
                data_type=f"discover_{category or 'all'}_{sort}",
                data=products,
                metadata={
                    "total_count": len(products),
                    "limit": limit,
                    "category": category,
                    "sort": sort,
                    "source": "gumroad.com",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Gumroad discover products: {e}")
            return self._create_response(
                success=False,
                data_type=f"discover_{category or 'all'}_{sort}",
                data=[],
                error=str(e),
            )

    async def fetch_category_products(
        self,
        category: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch products from a specific Gumroad category.

        Args:
            category: Product category (e.g., 'programming', 'design', 'software')
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with products from the category
        """
        return await self.fetch_discover_products(
            category=category,
            sort="featured",
            limit=limit,
            use_cache=use_cache,
        )

    async def fetch_programming_products(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch programming-related products (code, tutorials, courses).

        Args:
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with programming products
        """
        return await self.fetch_discover_products(
            category="programming",
            sort="featured",
            limit=limit,
            use_cache=use_cache,
        )

    async def fetch_design_products(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch design-related products (templates, assets, courses).

        Args:
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with design products
        """
        return await self.fetch_discover_products(
            category="design",
            sort="featured",
            limit=limit,
            use_cache=use_cache,
        )

    async def fetch_software_products(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch software products (apps, tools, plugins).

        Args:
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with software products
        """
        return await self.fetch_discover_products(
            category="software",
            sort="featured",
            limit=limit,
            use_cache=use_cache,
        )

    async def fetch_business_products(
        self,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch business-related products (templates, courses, ebooks).

        Args:
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with business products
        """
        return await self.fetch_discover_products(
            category="business",
            sort="featured",
            limit=limit,
            use_cache=use_cache,
        )

    async def search_products(
        self,
        query: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Search for products on Gumroad.

        Args:
            query: Search query
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with search results
        """
        return await self.fetch_with_cache(
            data_type=f"search_{query}",
            fetch_func=self._search_products_internal,
            use_cache=use_cache,
            query=query,
            limit=min(limit, 50),
        )

    async def _search_products_internal(
        self,
        query: str,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to search products."""
        try:
            encoded_query = quote_plus(query)
            # Gumroad uses ?query= for search
            url = f"{self.DISCOVER_URL}?query={encoded_query}"

            logger.info(f"Searching Gumroad for '{query}'")

            import httpx
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(
                    url,
                    timeout=15.0,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    },
                )

            if response.status_code != 200:
                return self._create_response(
                    success=False,
                    data_type=f"search_{query}",
                    data=[],
                    error=f"Failed to search: HTTP {response.status_code}",
                )

            products = self._parse_discover_page(response.text, limit, None)

            return self._create_response(
                success=True,
                data_type=f"search_{query}",
                data=products,
                metadata={
                    "total_count": len(products),
                    "limit": limit,
                    "query": query,
                    "source": "gumroad.com",
                },
            )

        except Exception as e:
            logger.error(f"Error searching Gumroad for '{query}': {e}")
            return self._create_response(
                success=False,
                data_type=f"search_{query}",
                data=[],
                error=str(e),
            )

    async def fetch_creator_products(
        self,
        creator_username: str,
        limit: int = 20,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch products from a specific creator.

        Args:
            creator_username: Creator's Gumroad username
            limit: Number of products to fetch
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with creator's products
        """
        return await self.fetch_with_cache(
            data_type=f"creator_{creator_username}",
            fetch_func=self._fetch_creator_products_internal,
            use_cache=use_cache,
            creator_username=creator_username,
            limit=min(limit, 50),
        )

    async def _fetch_creator_products_internal(
        self,
        creator_username: str,
        limit: int = 20,
    ) -> TrendingResponse:
        """Internal implementation to fetch creator products."""
        try:
            url = f"{self.BASE_URL}/{creator_username}"

            logger.info(f"Fetching Gumroad creator @{creator_username} from {url}")

            import httpx
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(
                    url,
                    timeout=15.0,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    },
                )

            if response.status_code != 200:
                return self._create_response(
                    success=False,
                    data_type=f"creator_{creator_username}",
                    data=[],
                    error=f"Failed to fetch: HTTP {response.status_code}",
                )

            products = self._parse_creator_page(
                response.text, limit, creator_username
            )

            return self._create_response(
                success=True,
                data_type=f"creator_{creator_username}",
                data=products,
                metadata={
                    "total_count": len(products),
                    "limit": limit,
                    "creator": creator_username,
                    "source": "gumroad.com",
                },
            )

        except Exception as e:
            logger.error(f"Error fetching Gumroad creator @{creator_username}: {e}")
            return self._create_response(
                success=False,
                data_type=f"creator_{creator_username}",
                data=[],
                error=str(e),
            )

    def _parse_discover_page(
        self, html: str, limit: int, category: str | None
    ) -> list[GumroadProduct]:
        """Parse products from Gumroad discover page."""
        products = []
        soup = BeautifulSoup(html, "html.parser")

        # Find product cards - Gumroad uses article.product-card
        product_cards = soup.select("article.product-card")

        for i, card in enumerate(product_cards[:limit]):
            try:
                product = self._parse_product_card_v2(card, i + 1, category)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing Gumroad product card: {e}")
                continue

        # If no products found with selectors, try JSON data
        if not products:
            products = self._parse_json_data(html, limit, category)

        return products

    def _parse_product_card_v2(
        self, card, rank: int, category: str | None
    ) -> GumroadProduct | None:
        """Parse a single product card from Gumroad's current HTML structure."""
        try:
            # Get product link and name from h2 inside stretched-link
            link_elem = card.select_one("a.stretched-link")
            if not link_elem:
                return None

            url = link_elem.get("href", "")
            
            # Extract product ID from URL (e.g., /l/GVbMo)
            product_id = ""
            if "/l/" in url:
                product_id = url.split("/l/")[-1].split("?")[0]

            # Get name from h2
            name_elem = link_elem.select_one("h2")
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"

            # Get description from small tag
            desc_elem = card.select_one("small")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Get creator info from a.user
            creator_elem = card.select_one("a.user")
            creator_name = ""
            creator_url = ""
            if creator_elem:
                # Creator name is text content (excluding img)
                creator_name = creator_elem.get_text(strip=True)
                creator_url = creator_elem.get("href", "")

            # Get price from the price div
            price_elem = card.select_one("[itemprop='price']")
            price_text = price_elem.get_text(strip=True) if price_elem else "$0+"
            price_cents = self._parse_price(price_text)

            # Get thumbnail
            img_elem = card.select_one("figure img")
            thumbnail_url = img_elem.get("src", "") if img_elem else ""

            # Get rating if available
            rating = 0.0
            ratings_count = 0
            rating_elem = card.select_one("[class*='rating']")
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r"(\d+\.?\d*)", rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))

            return GumroadProduct(
                rank=rank,
                id=product_id,
                name=name,
                description=description[:500] if description else "",
                url=url,
                price=price_text,
                price_cents=price_cents,
                creator_name=creator_name,
                creator_url=creator_url,
                thumbnail_url=thumbnail_url,
                rating=rating,
                ratings_count=ratings_count,
                sales_count=0,
                category=category or "",
                tags=[],
                is_featured=False,
            )

        except Exception as e:
            logger.warning(f"Error parsing product card v2: {e}")
            return None

    def _parse_product_card(
        self, card, rank: int, category: str | None
    ) -> GumroadProduct | None:
        """Parse a single product card."""
        try:
            # Get product URL and ID
            link = card.get("href") if card.name == "a" else None
            if not link:
                link_elem = card.select_one("a[href*='/l/']")
                link = link_elem.get("href") if link_elem else None

            if not link:
                return None

            # Extract product ID from URL
            product_id = link.split("/l/")[-1].split("?")[0] if "/l/" in link else ""

            # Full URL
            if link.startswith("/"):
                url = f"{self.BASE_URL}{link}"
            elif not link.startswith("http"):
                url = f"{self.BASE_URL}/{link}"
            else:
                url = link

            # Get product name
            name_elem = card.select_one("h3") or card.select_one(
                ".product-name"
            ) or card.select_one("[class*='name']") or card.select_one("strong")
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"

            # Get description
            desc_elem = card.select_one("p") or card.select_one(
                ".product-description"
            ) or card.select_one("[class*='description']")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Get price
            price_elem = card.select_one("[class*='price']") or card.select_one(
                ".price"
            ) or card.select_one("span[class*='amount']")
            price_text = price_elem.get_text(strip=True) if price_elem else "$0+"

            # Parse price to cents
            price_cents = self._parse_price(price_text)

            # Get creator info
            creator_elem = card.select_one("[class*='creator']") or card.select_one(
                "[class*='author']"
            ) or card.select_one("[class*='seller']")
            creator_name = (
                creator_elem.get_text(strip=True) if creator_elem else "Unknown"
            )

            creator_link = card.select_one("a[href^='/@']") or card.select_one(
                "a[href*='gumroad.com/']"
            )
            creator_url = ""
            if creator_link:
                href = creator_link.get("href", "")
                if href.startswith("/"):
                    creator_url = f"{self.BASE_URL}{href}"
                else:
                    creator_url = href

            # Get thumbnail
            img_elem = card.select_one("img")
            thumbnail_url = img_elem.get("src", "") if img_elem else ""

            # Get rating
            rating_elem = card.select_one("[class*='rating']") or card.select_one(
                "[class*='stars']"
            )
            rating = 0.0
            ratings_count = 0
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r"(\d+\.?\d*)", rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
                count_match = re.search(r"\((\d+)\)", rating_text)
                if count_match:
                    ratings_count = int(count_match.group(1))

            return GumroadProduct(
                rank=rank,
                id=product_id,
                name=name,
                description=description,
                url=url,
                price=price_text,
                price_cents=price_cents,
                creator_name=creator_name,
                creator_url=creator_url,
                thumbnail_url=thumbnail_url,
                rating=rating,
                ratings_count=ratings_count,
                sales_count=0,  # Not available from card
                category=category or "",
                tags=[],
                is_featured=False,
            )

        except Exception as e:
            logger.warning(f"Error parsing product card: {e}")
            return None

    def _parse_json_data(
        self, html: str, limit: int, category: str | None
    ) -> list[GumroadProduct]:
        """Try to parse products from embedded JSON data."""
        products = []

        # Look for JSON data in script tags
        import json

        soup = BeautifulSoup(html, "html.parser")

        for script in soup.select("script"):
            script_text = script.string or ""
            if "products" in script_text.lower() and "{" in script_text:
                try:
                    # Try to find JSON object
                    json_match = re.search(r"\{.*\"products\".*\}", script_text, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group())
                        if "products" in data:
                            for i, item in enumerate(data["products"][:limit]):
                                product = self._parse_json_product(
                                    item, i + 1, category
                                )
                                if product:
                                    products.append(product)
                except (json.JSONDecodeError, KeyError):
                    continue

        return products

    def _parse_json_product(
        self, data: dict, rank: int, category: str | None
    ) -> GumroadProduct | None:
        """Parse a product from JSON data."""
        try:
            return GumroadProduct(
                rank=rank,
                id=data.get("id", ""),
                name=data.get("name", "") or data.get("title", ""),
                description=data.get("description", "") or data.get("summary", ""),
                url=data.get("url", "") or data.get("permalink", ""),
                price=data.get("formatted_price", "") or data.get("price", "$0+"),
                price_cents=data.get("price_cents", 0),
                creator_name=data.get("creator", {}).get("name", "")
                or data.get("seller_name", ""),
                creator_url=data.get("creator", {}).get("url", "")
                or data.get("seller_url", ""),
                thumbnail_url=data.get("thumbnail_url", "")
                or data.get("cover_url", ""),
                rating=data.get("rating", 0) or 0,
                ratings_count=data.get("ratings_count", 0) or 0,
                sales_count=data.get("sales_count", 0) or 0,
                category=category or data.get("category", ""),
                tags=data.get("tags", []),
                is_featured=data.get("is_featured", False),
            )
        except Exception as e:
            logger.warning(f"Error parsing JSON product: {e}")
            return None

    def _parse_creator_page(
        self, html: str, limit: int, creator_username: str
    ) -> list[GumroadProduct]:
        """Parse products from a creator's page."""
        products = []
        soup = BeautifulSoup(html, "html.parser")

        # Get creator name from page
        creator_name_elem = soup.select_one("h1") or soup.select_one(
            "[class*='profile-name']"
        )
        creator_name = (
            creator_name_elem.get_text(strip=True)
            if creator_name_elem
            else creator_username
        )
        creator_url = f"{self.BASE_URL}/{creator_username}"

        # Find product cards
        product_cards = soup.select("article") or soup.select(
            "[class*='product']"
        ) or soup.select("a[href*='/l/']")

        for i, card in enumerate(product_cards[:limit]):
            try:
                product = self._parse_product_card(card, i + 1, None)
                if product:
                    # Override creator info
                    product.creator_name = creator_name
                    product.creator_url = creator_url
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing creator product: {e}")
                continue

        return products

    def _parse_price(self, price_text: str) -> int:
        """Parse price text to cents."""
        if not price_text:
            return 0

        # Handle free products
        if "free" in price_text.lower() or price_text == "$0":
            return 0

        # Handle "pay what you want" ($0+)
        if "$0+" in price_text or "+" in price_text:
            return 0

        # Extract numeric value
        match = re.search(r"[\$€£]?(\d+(?:[.,]\d{1,2})?)", price_text)
        if match:
            price_str = match.group(1).replace(",", ".")
            try:
                return int(float(price_str) * 100)
            except ValueError:
                return 0

        return 0


"""We Work Remotely fetcher implementation.

We Work Remotely is the largest remote work community in the world.
It provides RSS feeds for different job categories.

RSS Feeds:
- Programming: https://weworkremotely.com/categories/remote-programming-jobs.rss
- Design: https://weworkremotely.com/categories/remote-design-jobs.rss
- DevOps: https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss
- All: https://weworkremotely.com/remote-jobs.rss
"""

import re
from datetime import datetime

from ...models import TrendingResponse
from ...models.weworkremotely import WeWorkRemotelyJob
from ...utils import logger
from ..base import BaseFetcher


class WeWorkRemotelyFetcher(BaseFetcher):
    """Fetcher for We Work Remotely job listings."""

    # Category to RSS feed mapping
    CATEGORY_FEEDS = {
        "programming": "remote-programming-jobs",
        "design": "remote-design-jobs",
        "devops": "remote-devops-sysadmin-jobs",
        "management": "remote-management-exec-jobs",
        "sales": "remote-sales-marketing-jobs",
        "customer-support": "remote-customer-support-jobs",
        "finance": "remote-finance-legal-jobs",
        "product": "remote-product-jobs",
        "all": "remote-jobs",
    }

    def __init__(self, **kwargs):
        """Initialize We Work Remotely fetcher."""
        super().__init__(**kwargs)
        self.base_url = "https://weworkremotely.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "weworkremotely"

    async def fetch_jobs(
        self,
        category: str = "programming",
        limit: int = 30,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch remote job listings from We Work Remotely.

        Args:
            category: Job category ('programming', 'design', 'devops', 'management',
                     'sales', 'customer-support', 'finance', 'product', 'all')
            limit: Number of jobs to fetch (max 100)
            use_cache: Whether to use cached data

        Returns:
            TrendingResponse with job listings
        """
        # Normalize category
        category_lower = category.lower().strip()
        if category_lower not in self.CATEGORY_FEEDS:
            category_lower = "programming"  # Default to programming

        return await self.fetch_with_cache(
            data_type=f"jobs_{category_lower}",
            fetch_func=self._fetch_jobs_internal,
            use_cache=use_cache,
            category=category_lower,
            limit=min(limit, 100),
        )

    async def _fetch_jobs_internal(
        self, category: str = "programming", limit: int = 30
    ) -> TrendingResponse:
        """Internal implementation to fetch job listings."""
        try:
            feed_name = self.CATEGORY_FEEDS.get(category, "remote-programming-jobs")

            if category == "all":
                url = f"{self.base_url}/{feed_name}.rss"
            else:
                url = f"{self.base_url}/categories/{feed_name}.rss"

            logger.info(f"Fetching We Work Remotely jobs from {url}")

            response = await self.http_client.get(url)
            rss_content = response.text

            jobs = self._parse_rss(rss_content, category, limit)

            return self._create_response(
                success=True,
                data_type=f"jobs_{category}",
                data=jobs,
                metadata={
                    "category": category,
                    "total_count": len(jobs),
                    "limit": limit,
                    "source": "weworkremotely.com",
                    "available_categories": list(self.CATEGORY_FEEDS.keys()),
                },
            )

        except Exception as e:
            logger.error(f"Error fetching We Work Remotely jobs: {e}")
            return self._create_response(
                success=False,
                data_type=f"jobs_{category}",
                data=[],
                error=str(e),
                metadata={
                    "available_categories": list(self.CATEGORY_FEEDS.keys()),
                },
            )

    def _parse_rss(self, rss_content: str, category: str, limit: int) -> list[WeWorkRemotelyJob]:
        """Parse RSS feed content."""
        jobs = []

        try:
            # Simple XML parsing using regex (to avoid additional dependencies)
            items = re.findall(r"<item>(.*?)</item>", rss_content, re.DOTALL)

            for i, item in enumerate(items[:limit]):
                try:
                    # Extract fields using regex
                    title_match = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
                    if not title_match:
                        title_match = re.search(r"<title>(.*?)</title>", item)
                    title = title_match.group(1) if title_match else ""

                    link_match = re.search(r"<link>(.*?)</link>", item)
                    url = link_match.group(1) if link_match else ""

                    guid_match = re.search(r"<guid.*?>(.*?)</guid>", item)
                    job_id = guid_match.group(1) if guid_match else f"wwr-{i}"

                    pub_date_match = re.search(r"<pubDate>(.*?)</pubDate>", item)
                    pub_date_str = pub_date_match.group(1) if pub_date_match else ""

                    description_match = re.search(
                        r"<description><!\[CDATA\[(.*?)\]\]></description>", item, re.DOTALL
                    )
                    if not description_match:
                        description_match = re.search(
                            r"<description>(.*?)</description>", item, re.DOTALL
                        )
                    description = description_match.group(1) if description_match else ""

                    # Parse company from title (usually "Company: Position")
                    company = ""
                    position = title
                    if ":" in title:
                        parts = title.split(":", 1)
                        company = parts[0].strip()
                        position = parts[1].strip() if len(parts) > 1 else title

                    # Parse region from description
                    region = ""
                    region_match = re.search(r"Region:\s*([^<\n]+)", description)
                    if region_match:
                        region = region_match.group(1).strip()

                    # Parse published date
                    try:
                        # RFC 2822 format: "Mon, 25 Nov 2024 12:00:00 +0000"
                        published_at = datetime.strptime(
                            pub_date_str.strip(), "%a, %d %b %Y %H:%M:%S %z"
                        )
                    except (ValueError, AttributeError):
                        try:
                            # Try without timezone
                            published_at = datetime.strptime(
                                pub_date_str.strip()[:25], "%a, %d %b %Y %H:%M:%S"
                            )
                        except (ValueError, AttributeError):
                            published_at = datetime.now()

                    # Clean description (remove HTML tags)
                    clean_description = re.sub(r"<[^>]+>", "", description)
                    clean_description = clean_description[:500]  # Limit length

                    job = WeWorkRemotelyJob(
                        rank=i + 1,
                        id=job_id,
                        title=position,
                        company=company,
                        url=url,
                        published_at=published_at,
                        category=category,
                        region=region,
                        description=clean_description.strip(),
                        tags=[category, "remote"],
                    )
                    jobs.append(job)

                except Exception as e:
                    logger.warning(f"Error parsing We Work Remotely job item: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing We Work Remotely RSS: {e}")

        return jobs

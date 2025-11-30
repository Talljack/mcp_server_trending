"""RemoteOK jobs fetcher implementation."""

from datetime import datetime

from ...models.base import TrendingResponse
from ...models.remoteok import RemoteJob
from ...utils import logger
from ..base import BaseFetcher


class RemoteOKFetcher(BaseFetcher):
    """Fetcher for RemoteOK job data."""

    API_URL = "https://remoteok.com/api"
    BASE_URL = "https://remoteok.com"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "remoteok"

    async def fetch_jobs(
        self,
        tags: list[str] | None = None,
        search: str | None = None,
        limit: int = 50,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch remote jobs from RemoteOK.

        Args:
            tags: Filter by tags/skills (e.g., ['python', 'react'])
            search: Search keyword
            limit: Number of jobs to return (max 100)
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with job data
        """
        return await self.fetch_with_cache(
            data_type="jobs",
            fetch_func=self._fetch_jobs_internal,
            use_cache=use_cache,
            tags=tags,
            search=search,
            limit=limit,
        )

    async def _fetch_jobs_internal(
        self,
        tags: list[str] | None = None,
        search: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Internal method to fetch jobs."""
        # Limit to reasonable range
        limit = min(max(1, limit), 100)

        # Try API first, then fallback to web scraping
        try:
            return await self._fetch_from_api(tags, search, limit)
        except Exception as api_error:
            logger.warning(f"API fetch failed: {api_error}, trying web scraping...")
            try:
                return await self._fetch_from_web(tags, search, limit)
            except Exception as scrape_error:
                logger.error(f"Both API and web scraping failed: {scrape_error}")
                return self._create_response(
                    success=False,
                    data_type="jobs",
                    data=[],
                    error=f"Failed to fetch jobs. API error: {api_error}. Scraping error: {scrape_error}",
                )

    async def _fetch_from_api(
        self,
        tags: list[str] | None = None,
        search: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """
        Fetch jobs from RemoteOK official JSON API.

        API format (verified 2025-11-17):
        - URL: https://remoteok.com/api
        - Returns: JSON array
        - First element [0]: metadata/header (skip this)
        - Jobs start from [1]: actual job listings
        - Each job has: id, position, company, salary, tags, url, date, etc.
        """
        try:
            # RemoteOK official API - requires realistic browser headers
            # API is public but blocks VPN/proxy connections
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://remoteok.com/",
            }

            response = await self.http_client.get(self.API_URL, headers=headers)

            if response.status_code != 200:
                raise Exception(f"RemoteOK API returned status {response.status_code}")

            # Check if response is the VPN block message (plain text)
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type or "text/plain" in content_type:
                text = response.text
                if "VPN" in text or "vpn" in text:
                    raise Exception(
                        "RemoteOK is blocking VPN/proxy access. Please disable VPN or use a different network."
                    )
                raise Exception(f"Unexpected response type: {content_type}")

            # Parse JSON response
            data = response.json()

            if not isinstance(data, list) or len(data) == 0:
                raise Exception("Invalid API response format")

            # RemoteOK API format: first element [0] is metadata/header, skip it
            # Real jobs start from index [1]
            logger.info(f"RemoteOK API returned {len(data)} items (including header)")
            jobs_data = data[1:] if len(data) > 1 else []

            if not jobs_data:
                raise Exception("No job data found in API response")

            # Parse jobs with filtering
            jobs = self._parse_jobs(jobs_data, tags=tags, search=search, limit=limit)

            metadata = {
                "total_count": len(jobs),
                "total_available": len(jobs_data),
                "tags": tags,
                "search": search,
                "limit": limit,
                "url": self.BASE_URL,
                "source": "Official JSON API",
                "api_version": "2025-11",
            }

            logger.info(
                f"Successfully fetched {len(jobs)} jobs from RemoteOK API (filtered from {len(jobs_data)} total)"
            )

            return self._create_response(
                success=True,
                data_type="jobs",
                data=jobs,
                metadata=metadata,
            )

        except Exception as e:
            logger.warning(f"RemoteOK API fetch failed: {e}")
            raise

    async def _fetch_from_web(
        self,
        tags: list[str] | None = None,
        search: str | None = None,
        limit: int = 50,
    ) -> TrendingResponse:
        """Fetch jobs from RemoteOK website using Playwright."""
        logger.info("Fetching RemoteOK jobs using web scraping")

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Navigate to RemoteOK
                await page.goto("https://remoteok.com/", wait_until="domcontentloaded")

                # Wait for job listings to load
                await page.wait_for_selector("tr.job", timeout=10000)

                # Extract job data from the page
                jobs_data = await page.evaluate("""
                    () => {
                        const jobs = [];
                        const jobRows = document.querySelectorAll('tr.job');

                        jobRows.forEach((row, index) => {
                            const id = row.getAttribute('data-id') || `job-${index}`;
                            const url = row.getAttribute('data-url') || '';

                            const titleEl = row.querySelector('h2.title, a.preventLink');
                            const title = titleEl ? titleEl.textContent.trim() : '';

                            const companyEl = row.querySelector('h3.company, .company');
                            const company = companyEl ? companyEl.textContent.trim() : '';

                            const locationEl = row.querySelector('.location');
                            const location = locationEl ? locationEl.textContent.trim() : 'Remote';

                            const tagsEls = row.querySelectorAll('.tag');
                            const tags = Array.from(tagsEls).map(el => el.textContent.trim());

                            const dateEl = row.querySelector('time, .time');
                            const date = dateEl ? dateEl.getAttribute('datetime') || dateEl.textContent.trim() : '';

                            const salaryEl = row.querySelector('.salary, [data-salary]');
                            const salary = salaryEl ? salaryEl.textContent.trim() : '';

                            if (title && id) {
                                jobs.push({
                                    id: id,
                                    title: title,
                                    company: company,
                                    location: location,
                                    tags: tags,
                                    date: date,
                                    salary: salary,
                                    url: url ? `https://remoteok.com${url}` : `https://remoteok.com/remote-jobs/${id}`,
                                    description: '',
                                    logo: ''
                                });
                            }
                        });

                        return jobs;
                    }
                """)

                await browser.close()

                # Parse jobs
                jobs = self._parse_jobs(jobs_data, tags=tags, search=search, limit=limit)

                metadata = {
                    "total_count": len(jobs),
                    "tags": tags,
                    "search": search,
                    "limit": limit,
                    "url": self.BASE_URL,
                    "source": "Web Scraping",
                }

                logger.info(f"Successfully scraped {len(jobs)} jobs from RemoteOK")

                return self._create_response(
                    success=True,
                    data_type="jobs",
                    data=jobs,
                    metadata=metadata,
                )

        except Exception as e:
            logger.error(f"Web scraping failed: {e}", exc_info=True)
            raise

    def _parse_jobs(
        self,
        jobs_data: list[dict],
        tags: list[str] | None = None,
        search: str | None = None,
        limit: int = 50,
    ) -> list[RemoteJob]:
        """Parse job data from API response."""
        jobs = []

        for job_data in jobs_data:
            try:
                # Skip if not a valid job
                if not job_data.get("id"):
                    continue

                # Filter by tags if specified
                job_tags = job_data.get("tags", [])
                if tags:
                    tags_lower = [t.lower() for t in tags]
                    job_tags_lower = [t.lower() for t in job_tags]
                    if not any(tag in job_tags_lower for tag in tags_lower):
                        continue

                # Filter by search keyword if specified
                if search:
                    search_lower = search.lower()
                    title = job_data.get("position", "").lower()
                    description = job_data.get("description", "").lower()
                    company = job_data.get("company", "").lower()

                    if (
                        search_lower not in title
                        and search_lower not in description
                        and search_lower not in company
                    ):
                        continue

                # Parse salary
                salary_min = job_data.get("salary_min")
                salary_max = job_data.get("salary_max")

                # Build salary display
                salary_display = None
                if salary_min and salary_max:
                    salary_display = f"${salary_min:,} - ${salary_max:,}"
                elif salary_min:
                    salary_display = f"${salary_min:,}+"
                elif salary_max:
                    salary_display = f"Up to ${salary_max:,}"

                # Parse date
                posted_date = None
                epoch = job_data.get("epoch")
                if epoch:
                    try:
                        posted_date = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d")
                    except:
                        pass

                # Build apply URL
                slug = job_data.get("slug")
                job_url = f"{self.BASE_URL}/remote-jobs/{slug}" if slug else f"{self.BASE_URL}"

                apply_url = job_data.get("apply_url")

                job = RemoteJob(
                    rank=len(jobs) + 1,
                    id=str(job_data.get("id", "")),
                    title=job_data.get("position", ""),
                    company=job_data.get("company", ""),
                    company_logo=job_data.get("company_logo"),
                    description=job_data.get("description", "")[:500],  # Truncate description
                    location=job_data.get("location", "Anywhere"),
                    tags=job_tags[:15],  # Limit tags
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_display=salary_display,
                    url=job_url,
                    apply_url=apply_url,
                    posted_date=posted_date,
                    is_featured=job_data.get("featured", False),
                    job_type=job_data.get("type", "full-time"),
                )

                jobs.append(job)

                # Stop if we've reached the limit
                if len(jobs) >= limit:
                    break

            except Exception as e:
                logger.warning(f"Error parsing job {job_data.get('id', 'unknown')}: {e}")
                continue

        return jobs

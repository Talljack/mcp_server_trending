"""GitHub Trending fetcher implementation."""

from typing import List, Optional

from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher
from models.base import TrendingResponse
from models.github import GitHubDeveloper, GitHubRepository
from utils import logger


class GitHubTrendingFetcher(BaseFetcher):
    """Fetcher for GitHub Trending data."""

    BASE_URL = "https://github.com/trending"

    def get_platform_name(self) -> str:
        """Get platform name."""
        return "github"

    async def fetch_trending_repositories(
        self,
        time_range: str = "daily",
        language: Optional[str] = None,
        spoken_language: Optional[str] = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch GitHub trending repositories.

        Args:
            time_range: Time range (daily, weekly, monthly)
            language: Programming language filter
            spoken_language: Spoken language filter
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with repository data
        """
        return await self.fetch_with_cache(
            data_type="trending_repos",
            fetch_func=self._fetch_repos_internal,
            use_cache=use_cache,
            time_range=time_range,
            language=language,
            spoken_language=spoken_language,
        )

    async def _fetch_repos_internal(
        self,
        time_range: str = "daily",
        language: Optional[str] = None,
        spoken_language: Optional[str] = None,
    ) -> TrendingResponse:
        """Internal method to fetch repositories."""
        try:
            # Build URL with parameters
            params = {}
            if language:
                params['language'] = language
            if spoken_language:
                params['spoken_language_code'] = spoken_language

            # Map time_range to GitHub's since parameter
            since_map = {
                "daily": "daily",
                "weekly": "weekly",
                "monthly": "monthly"
            }
            params['since'] = since_map.get(time_range, "daily")

            # Fetch HTML page
            response = await self.http_client.get(
                self.BASE_URL,
                params=params,
            )

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            repos = self._parse_repositories(soup)

            metadata = {
                "total_count": len(repos),
                "time_range": time_range,
                "language": language,
                "spoken_language": spoken_language,
            }

            return self._create_response(
                success=True,
                data_type="trending_repos",
                data=repos,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching GitHub trending repos: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_repos",
                data=[],
                error=str(e),
            )

    def _parse_repositories(self, soup: BeautifulSoup) -> List[GitHubRepository]:
        """Parse repository data from HTML."""
        repos = []
        articles = soup.find_all('article', class_='Box-row')

        for rank, article in enumerate(articles, 1):
            try:
                # Repository name and author
                h2 = article.find('h2', class_='h3')
                if not h2:
                    continue

                link = h2.find('a')
                if not link:
                    continue

                href = link.get('href', '')
                parts = href.strip('/').split('/')
                if len(parts) < 2:
                    continue

                author, name = parts[0], parts[1]

                # Description
                description_elem = article.find('p', class_='col-9')
                description = description_elem.get_text(strip=True) if description_elem else ""

                # Language
                language = None
                language_color = None
                lang_elem = article.find('span', itemprop='programmingLanguage')
                if lang_elem:
                    language = lang_elem.get_text(strip=True)
                    color_span = lang_elem.find_previous_sibling('span')
                    if color_span and 'style' in color_span.attrs:
                        # Extract color from style
                        style = color_span['style']
                        if 'background-color:' in style:
                            language_color = style.split('background-color:')[1].split(';')[0].strip()

                # Stars (total)
                stars = 0
                star_elem = article.find('svg', class_='octicon-star')
                if star_elem:
                    star_parent = star_elem.find_parent('a')
                    if star_parent:
                        star_text = star_parent.get_text(strip=True)
                        stars = self._parse_number(star_text)

                # Forks
                forks = 0
                fork_elem = article.find('svg', class_='octicon-repo-forked')
                if fork_elem:
                    fork_parent = fork_elem.find_parent('a')
                    if fork_parent:
                        fork_text = fork_parent.get_text(strip=True)
                        forks = self._parse_number(fork_text)

                # Stars today
                stars_today = 0
                stars_today_elem = article.find('span', class_='float-sm-right')
                if stars_today_elem:
                    stars_today_text = stars_today_elem.get_text(strip=True)
                    stars_today = self._parse_number(stars_today_text.split('stars')[0])

                # Built by (contributors)
                built_by = []
                built_by_elem = article.find('span', string=lambda text: text and 'Built by' in text)
                if built_by_elem:
                    avatars = built_by_elem.find_parent().find_all('img')
                    built_by = [img.get('alt', '').strip('@') for img in avatars if img.get('alt')]

                repo = GitHubRepository(
                    rank=rank,
                    author=author,
                    name=name,
                    url=f"https://github.com{href}",
                    description=description,
                    language=language,
                    language_color=language_color,
                    stars=stars,
                    forks=forks,
                    stars_today=stars_today,
                    built_by=built_by,
                )
                repos.append(repo)

            except Exception as e:
                logger.warning(f"Error parsing repository at rank {rank}: {e}")
                continue

        return repos

    async def fetch_trending_developers(
        self,
        time_range: str = "daily",
        language: Optional[str] = None,
        use_cache: bool = True,
    ) -> TrendingResponse:
        """
        Fetch GitHub trending developers.

        Args:
            time_range: Time range (daily, weekly, monthly)
            language: Programming language filter
            use_cache: Whether to use cache

        Returns:
            TrendingResponse with developer data
        """
        return await self.fetch_with_cache(
            data_type="trending_developers",
            fetch_func=self._fetch_developers_internal,
            use_cache=use_cache,
            time_range=time_range,
            language=language,
        )

    async def _fetch_developers_internal(
        self,
        time_range: str = "daily",
        language: Optional[str] = None,
    ) -> TrendingResponse:
        """Internal method to fetch developers."""
        try:
            # Build URL
            url = f"{self.BASE_URL}/developers"
            params = {}
            if language:
                params['language'] = language

            since_map = {
                "daily": "daily",
                "weekly": "weekly",
                "monthly": "monthly"
            }
            params['since'] = since_map.get(time_range, "daily")

            # Fetch HTML page
            response = await self.http_client.get(url, params=params)

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            developers = self._parse_developers(soup)

            metadata = {
                "total_count": len(developers),
                "time_range": time_range,
                "language": language,
            }

            return self._create_response(
                success=True,
                data_type="trending_developers",
                data=developers,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching GitHub trending developers: {e}", exc_info=True)
            return self._create_response(
                success=False,
                data_type="trending_developers",
                data=[],
                error=str(e),
            )

    def _parse_developers(self, soup: BeautifulSoup) -> List[GitHubDeveloper]:
        """Parse developer data from HTML."""
        developers = []
        articles = soup.find_all('article', class_='Box-row')

        for rank, article in enumerate(articles, 1):
            try:
                # Developer username and name
                h1 = article.find('h1', class_='h3')
                if not h1:
                    continue

                link = h1.find('a')
                if not link:
                    continue

                username = link.get_text(strip=True)
                href = link.get('href', '')

                # Full name
                name_elem = h1.find('span', class_='f4')
                name = name_elem.get_text(strip=True) if name_elem else username

                # Avatar
                avatar = ""
                img = article.find('img', class_='avatar')
                if img:
                    avatar = img.get('src', '')

                # Popular repo (if available)
                repo_name = None
                repo_description = None
                repo_elem = article.find('article', class_='mt-3')
                if repo_elem:
                    repo_link = repo_elem.find('a')
                    if repo_link:
                        repo_name = repo_link.get_text(strip=True)
                    desc_elem = repo_elem.find('div', class_='f6')
                    if desc_elem:
                        repo_description = desc_elem.get_text(strip=True)

                developer = GitHubDeveloper(
                    rank=rank,
                    username=username,
                    name=name,
                    url=f"https://github.com{href}",
                    avatar=avatar,
                    repo_name=repo_name,
                    repo_description=repo_description,
                )
                developers.append(developer)

            except Exception as e:
                logger.warning(f"Error parsing developer at rank {rank}: {e}")
                continue

        return developers

    @staticmethod
    def _parse_number(text: str) -> int:
        """Parse number from text (handles k, m suffixes)."""
        try:
            text = text.strip().replace(',', '')
            if 'k' in text.lower():
                return int(float(text.lower().replace('k', '')) * 1000)
            elif 'm' in text.lower():
                return int(float(text.lower().replace('m', '')) * 1000000)
            else:
                return int(text)
        except (ValueError, AttributeError):
            return 0

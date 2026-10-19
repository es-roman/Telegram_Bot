import aiohttp
from bot.models.search_result import SearchResult
import asyncio

MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def search_github(query: str) -> list[SearchResult]:
    results = []
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 5,
        "sort": "stars",
        "order": "desc",
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "TelegramGitHubBot/1.0",
    }

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                response.raise_for_status()
                data = await response.json()

    repositories = data["items"]

    for repo in repositories:
        name = repo["full_name"]
        description = repo["description"]
        language = repo["language"] or "Не указан"
        stars = repo["stargazers_count"]
        link = repo["html_url"]
        result = SearchResult(
            title=name,
            description=description,
            url=link,
            source="GitHub",
            language=language,
            stars=stars
        )
        results.append(result)

    return results

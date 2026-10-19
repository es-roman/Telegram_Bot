import asyncio

import aiohttp

from bot.models.search_result import SearchResult

MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def search_wikipedia(query: str) -> list[SearchResult]:
    results = []
    url = "https://ru.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": 5,
        "prop": "info|description",
        "inprop": "url",
        "format": "json",
        "formatversion": "2",
    }

    async with (
        semaphore,
        aiohttp.ClientSession() as session,
        session.get(
            url,
            params=params,
            headers={
                "User-Agent": (
                    "TelegramWikiBot/1.0 "
                    "(educational project; contact: your-email@example.com)"
                )
            },
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response,
    ):
        response.raise_for_status()
        data = await response.json()

    pages = data.get("query", {}).get("pages", [])

    for page in pages:
        result = SearchResult(
            title=page.get("title", "Без названия"),
            description=page.get("description"),
            url=page.get("fullurl", ""),
            source="Wikipedia",
        )
        results.append(result)

    return results

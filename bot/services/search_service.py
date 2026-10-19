import asyncio
from bot.models.search_result import SearchResult
from bot.providers.wikipedia import search_wikipedia
from bot.providers.github import search_github
from bot.providers.stackoverflow import search_stackoverflow


class SearchUnavailableError(Exception):
    pass


async def search_all(query: str) -> list[SearchResult]:
    search = []
    results = await asyncio.gather(search_wikipedia(query),
                                   search_github(query),
                                   search_stackoverflow(query),
                                   return_exceptions=True
                                   )

    if all(isinstance(result, Exception) for result in results):
        raise SearchUnavailableError(results)

    for result in results:
        if isinstance(result, Exception):
            continue

        search.extend(result)

    if not search:
        return []

    return search

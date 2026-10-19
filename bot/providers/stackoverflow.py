import aiohttp
from bot.models.search_result import SearchResult
import asyncio

MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def search_stackoverflow(query: str) -> list[SearchResult]:
    results = []
    url = "https://api.stackexchange.com/2.3/search/advanced"

    params = {
        "site": "stackoverflow",
        "q": query,
        "pagesize": 5,
        "sort": "relevance",
        "order": "desc",
    }

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                response.raise_for_status()
                data = await response.json()

    questions = data.get("items", [])

    for question in questions:
        name = question["title"]
        link = question["link"]
        score = question.get("score", 0)
        answers = question.get("answer_count", 0)
        answered = question.get("is_answered", False)

        status = "Есть принятый ответ" if answered else "Нет принятого ответа"

        result = SearchResult(
            title=name,
            url=link,
            source="StackOverflow",
            score=score,
            answers=answers,
            status=status
        )

        results.append(result)

    return results

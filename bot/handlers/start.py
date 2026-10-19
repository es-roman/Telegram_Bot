from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Напиши тему, и я найду статьи в Википедии."
    )

# #================================================
# #===================ВИКИПЕДИЯ====================
# #================================================
#
# # @router.message()
# # async def search_wikipedia(message: Message) -> None:
# #     query = message.text
# #
# #     if not query:
# #         await message.answer("Отправь текстовый поисковый запрос.")
# #         return
# #
# #     url = "https://ru.wikipedia.org/w/api.php"
# #
# #     params = {
# #         "action": "query",
# #         "list": "search",
# #         "srsearch": query,
# #         "srlimit": 5,
# #         "format": "json",
# #     }
# #
# #     try:
# #         async with aiohttp.ClientSession() as session:
# #             async with session.get(
# #                 url,
# #                 params=params,
# #                 headers={
# #                     "User-Agent": "TelegramWikiBot/1.0 (educational project; contact: your-email@example.com)"
# #                 },
# #                 timeout=aiohttp.ClientTimeout(total=10),
# #             ) as response:
# #                 response.raise_for_status()
# #                 data = await response.json()
# #
# #         results = data["query"]["search"]
# #
# #         if not results:
# #             await message.answer("Ничего не найдено.")
# #             return
# #
# #         answer = ["Нашёл статьи в Википедии:\n"]
# #
# #         for article in results:
# #             title = article["title"]
# #             link = (
# #                 "https://ru.wikipedia.org/wiki/"
# #                 + title.replace(" ", "_")
# #             )
# #             answer.append(f"• {title}\n{link}")
# #
# #         await message.answer("\n\n".join(answer))
# #
# #     # except Exception as error:
# #     #     print(f"Ошибка поиска в Википедии: {error!r}")
# #     # await message.answer(
# #     #     "Не удалось связаться с Википедией. Попробуй позже."
# #     # )
# #     except (aiohttp.ClientError, TimeoutError):
# #         await message.answer(
# #             "Не удалось связаться с Википедией. Попробуй позже."
# #         )
#
#
# #=============================================
# #===================ГИТХАБ====================
# #=============================================
#
# # @router.message()
# # async def search_github(message: Message) -> None:
# #     query = message.text
# #
# #     if not query:
# #         await message.answer("Отправь текстовый поисковый запрос.")
# #         return
# #
# #     url = "https://api.github.com/search/repositories"
# #
# #     params = {
# #         "q": query,
# #         "per_page": 5,
# #         "sort": "stars",
# #         "order": "desc",
# #     }
# #
# #     headers = {
# #         "Accept": "application/vnd.github+json",
# #         "User-Agent": "TelegramGitHubBot/1.0",
# #     }
# #
# #     try:
# #         async with aiohttp.ClientSession() as session:
# #             async with session.get(
# #                 url,
# #                 params=params,
# #                 headers=headers,
# #                 timeout=aiohttp.ClientTimeout(total=10),
# #             ) as response:
# #                 response.raise_for_status()
# #                 data = await response.json()
# #
# #         repositories = data["items"]
# #
# #         if not repositories:
# #             await message.answer("Репозитории не найдены.")
# #             return
# #
# #         answer = ["Нашёл репозитории на GitHub:\n"]
# #
# #         for repo in repositories:
# #             name = repo["full_name"]
# #             description = repo["description"] or "Описание отсутствует"
# #             language = repo["language"] or "Не указан"
# #             stars = repo["stargazers_count"]
# #             link = repo["html_url"]
# #
# #             answer.append(
# #                 f"**{name}**\n"
# #                 f"{description}\n"
# #                 f"Язык: {language} | ⭐ {stars}\n"
# #                 f"{link}"
# #             )
# #
# #         await message.answer("\n\n".join(answer))
# #
# #     except (aiohttp.ClientError, TimeoutError) as error:
# #         print(f"Ошибка поиска в GitHub: {error!r}")
# #         await message.answer(
# #             "Не удалось связаться с GitHub. Попробуй позже."
# #         )
#
#
# #=====================================================
# #===================Stack Overflow====================
# #=====================================================
#
#
#
# @router.message()
# async def search_stackoverflow(message: Message) -> None:
#     query = message.text
#
#     if not query:
#         await message.answer("Отправь текстовый поисковый запрос.")
#         return
#
#     url = "https://api.stackexchange.com/2.3/search/advanced"
#
#     params = {
#         "site": "stackoverflow",
#         "q": query,
#         "pagesize": 5,
#         "sort": "relevance",
#         "order": "desc",
#     }
#
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 url,
#                 params=params,
#                 timeout=aiohttp.ClientTimeout(total=10),
#             ) as response:
#                 response.raise_for_status()
#                 data = await response.json()
#
#         if "error_message" in data:
#             print(f"Ошибка Stack Exchange API: {data['error_message']}")
#             await message.answer("Сервис поиска вернул ошибку.")
#             return
#
#         questions = data.get("items", [])
#
#         if not questions:
#             await message.answer("По твоему запросу вопросы не найдены.")
#             return
#
#         answer = ["Нашёл вопросы на Stack Overflow:\n"]
#
#         for question in questions:
#             title = question["title"]
#             link = question["link"]
#             score = question.get("score", 0)
#             answers = question.get("answer_count", 0)
#             answered = question.get("is_answered", False)
#
#             status = "Есть принятый ответ" if answered else "Нет принятого ответа"
#
#             answer.append(
#                 f"{title}\n"
#                 f"⭐ Голоса: {score} | Ответов: {answers}\n"
#                 f"{status}\n"
#                 f"{link}"
#             )
#
#         await message.answer("\n\n".join(answer))
#
#     except (aiohttp.ClientError, TimeoutError) as error:
#         print(f"Ошибка поиска на Stack Overflow: {error!r}")
#         await message.answer(
#             "Не удалось связаться со Stack Overflow. Попробуй позже."
#         )

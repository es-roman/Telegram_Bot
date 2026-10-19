from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message

from bot.formatters.search_formatter import format_search_results
from bot.services.search_service import SearchUnavailableError, search_all

router = Router(name="search")


@router.message(F.text & ~F.text.startswith("/"))
async def any_message(message: Message) -> None:
    try:
        results = await search_all(message.text)
    except SearchUnavailableError:
        await message.answer("Источники временно недоступны")
        return

    if not results:
        await message.answer("Ничего не найдено.")
        return

    formatted_results = format_search_results(results)
    await message.answer(formatted_results, parse_mode=ParseMode.HTML)

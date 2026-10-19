
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from bot.handlers.search import any_message
from bot.models.search_result import SearchResult
from bot.services.search_service import SearchUnavailableError


@pytest.fixture
def message():
    """Создаёт фиктивное сообщение от пользователя."""
    msg = MagicMock()
    msg.text = "Python"
    msg.answer = AsyncMock()
    return msg


@pytest.fixture
def search_result():
    """Создаёт фиктивный результат поиска."""
    return SearchResult(
        title="Python",
        description="Programming language",
        url="https://example.com/python",
        source="Wikipedia",
    )


@pytest.mark.asyncio
async def test_any_message_success(message, search_result):
    """При успешном поиске бот отправляет отформатированные результаты."""
    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            return_value=[search_result],
        ) as mock_search,
        patch(
            "bot.handlers.search.format_search_results",
            return_value="Готовый результат",
        ) as mock_formatter,
    ):
        await any_message(message)

    mock_search.assert_awaited_once_with("Python")
    mock_formatter.assert_called_once_with([search_result])
    message.answer.assert_awaited_once_with("Готовый результат")


@pytest.mark.asyncio
async def test_any_message_empty_results(message):
    """При пустом списке результатов бот сообщает, что ничего не найдено."""
    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            return_value=[],
        ) as mock_search,
        patch(
            "bot.handlers.search.format_search_results",
        ) as mock_formatter,
    ):
        await any_message(message)

    mock_search.assert_awaited_once_with("Python")
    mock_formatter.assert_not_called()
    message.answer.assert_awaited_once_with("Ничего не найдено.")


@pytest.mark.asyncio
async def test_any_message_search_unavailable(message):
    """Если поиск недоступен, бот сообщает об ошибке."""
    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            side_effect=SearchUnavailableError(),
        ) as mock_search,
        patch(
            "bot.handlers.search.format_search_results",
        ) as mock_formatter,
    ):
        await any_message(message)

    mock_search.assert_awaited_once_with("Python")
    mock_formatter.assert_not_called()
    message.answer.assert_awaited_once_with(
        "Источники временно недоступны"
    )


@pytest.mark.asyncio
async def test_any_message_multiple_results(message):
    """Все результаты поиска передаются форматтеру."""
    results = [
        SearchResult(
            title="Python",
            description="Programming language",
            url="https://example.com/python",
            source="Wikipedia",
        ),
        SearchResult(
            title="Asyncio",
            description="Asynchronous programming",
            url="https://example.com/asyncio",
            source="Wikipedia",
        ),
    ]

    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            return_value=results,
        ),
        patch(
            "bot.handlers.search.format_search_results",
            return_value="Два результата",
        ) as mock_formatter,
    ):
        await any_message(message)

    mock_formatter.assert_called_once_with(results)
    message.answer.assert_awaited_once_with("Два результата")


@pytest.mark.asyncio
async def test_any_message_passes_user_text(message, search_result):
    """В поиск передаётся именно текст сообщения пользователя."""
    message.text = "асинхронность в Python"

    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            return_value=[search_result],
        ) as mock_search,
        patch(
            "bot.handlers.search.format_search_results",
            return_value="Результат",
        ),
    ):
        await any_message(message)

    mock_search.assert_awaited_once_with("асинхронность в Python")


@pytest.mark.asyncio
async def test_any_message_does_not_send_partial_results_on_error(message):
    """При ошибке поиска отправляется сообщение об ошибке, а не результаты."""
    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            side_effect=SearchUnavailableError(),
        ),
        patch(
            "bot.handlers.search.format_search_results",
        ) as mock_formatter,
    ):
        await any_message(message)

    mock_formatter.assert_not_called()
    message.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_any_message_sends_formatted_text_unchanged(
    message, search_result
):
    """Обработчик отправляет текст форматтера без изменений."""
    formatted_text = "Заголовок\n\nОписание\nСсылка"

    with (
        patch(
            "bot.handlers.search.search_all",
            new_callable=AsyncMock,
            return_value=[search_result],
        ),
        patch(
            "bot.handlers.search.format_search_results",
            return_value=formatted_text,
        ),
    ):
        await any_message(message)

    message.answer.assert_awaited_once_with(formatted_text)

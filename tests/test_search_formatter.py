from bot.models.search_result import SearchResult
from bot.formatters.search_formatter import format_search_results


def test_format_search_results_one_result():
    result = SearchResult(
        title="Python",
        description="Programming language",
        url="https://example.com/python",
        source="Wikipedia",
    )

    formatted = format_search_results([result])

    assert "Wikipedia" in formatted
    assert "Python" in formatted
    assert "Programming language" in formatted
    assert "https://example.com/python" in formatted


def test_format_search_results_multiple_results():
    results = [
        SearchResult(
            title="Python",
            description="Programming language",
            url="https://example.com/python",
            source="Wikipedia",
        ),
        SearchResult(
            title="Aiogram",
            description="Telegram Bot framework",
            url="https://example.com/aiogram",
            source="GitHub",
        ),
    ]

    formatted = format_search_results(results)

    assert "Python" in formatted
    assert "Programming language" in formatted
    assert "https://example.com/python" in formatted

    assert "Aiogram" in formatted
    assert "Telegram Bot framework" in formatted
    assert "https://example.com/aiogram" in formatted


def test_format_search_results_optional_fields():
    result = SearchResult(
        title="Aiogram",
        description="Telegram Bot framework",
        url="https://example.com/aiogram",
        source="GitHub",
        language="Python",
        stars=1500,
        score=95,
        answers=12,
        status="Open",
    )

    formatted = format_search_results([result])

    assert "Python" in formatted
    assert "1500" in formatted
    assert "95" in formatted
    assert "12" in formatted
    assert "Open" in formatted


def test_format_search_results_without_optional_fields():
    result = SearchResult(
        title="Python",
        description="Programming language",
        url="https://example.com/python",
        source="Wikipedia",
    )

    formatted = format_search_results([result])

    assert "Python" in formatted
    assert "1500" not in formatted
    assert "Open" not in formatted


def test_format_search_results_empty_list():
    formatted = format_search_results([])

    assert isinstance(formatted, str)
    assert formatted.strip()


def test_format_search_results_optional_fields_with_zero():
    result = SearchResult(
        title="Example",
        description="Test result",
        url="https://example.com",
        source="GitHub",
        stars=0,
        score=0,
        answers=0,
    )

    formatted = format_search_results([result])

    assert "0" in formatted

def test_format_search_results_exact_format():
    result = SearchResult(
        title="Python",
        description="Programming language",
        url="https://example.com/python",
        source="Wikipedia",
    )

    formatted = format_search_results([result])

    expected = (
        "Нашёл результат поиска:\n\n\n"
        "[Wikipedia]\n"
        "Название: Python\n"
        "💡Описание: Programming language"
        "\n➡️Ссылка: https://example.com/python"
    )
    
    assert formatted == expected

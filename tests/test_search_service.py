import pytest

import bot.services.search_service as service
from bot.models.search_result import SearchResult
from bot.services.search_service import SearchUnavailableError
from unittest.mock import AsyncMock


def make_result(title: str, source: str) -> SearchResult:
    return SearchResult(
        title=title,
        description=f"Описание {title}",
        url=f"https://example.com/{title}",
        source=source,
    )


def mock_provider(monkeypatch, provider_name, results=None, error=None):
    async def fake_search(query: str) -> list[SearchResult]:
        if error is not None:
            raise error
        return results if results is not None else []

    monkeypatch.setattr(service, provider_name, fake_search)


@pytest.mark.asyncio
async def test_all_sources_return_results(monkeypatch):
    wiki = [make_result("Python", "Wikipedia")]
    github = [make_result("Python project", "GitHub")]
    stackoverflow = [make_result("Python question", "StackOverflow")]

    mock_provider(monkeypatch, "search_wikipedia", results=wiki)
    mock_provider(monkeypatch, "search_github", results=github)
    mock_provider(monkeypatch, "search_stackoverflow", results=stackoverflow)

    results = await service.search_all("Python")

    assert len(results) == 3
    assert results == wiki + github + stackoverflow


@pytest.mark.asyncio
async def test_one_source_fails(monkeypatch):
    github = [make_result("Python project", "GitHub")]
    stackoverflow = [make_result("Python question", "StackOverflow")]

    mock_provider(
        monkeypatch, "search_wikipedia",
        error=RuntimeError("Wikipedia unavailable"),
    )
    mock_provider(monkeypatch, "search_github", results=github)
    mock_provider(monkeypatch, "search_stackoverflow", results=stackoverflow)

    results = await service.search_all("Python")

    assert results == github + stackoverflow


@pytest.mark.asyncio
async def test_two_sources_fail(monkeypatch):
    stackoverflow = [make_result("Python question", "StackOverflow")]

    mock_provider(
        monkeypatch, "search_wikipedia",
        error=RuntimeError("Wikipedia unavailable"),
    )
    mock_provider(
        monkeypatch, "search_github",
        error=RuntimeError("GitHub unavailable"),
    )
    mock_provider(
        monkeypatch, "search_stackoverflow",
        results=stackoverflow,
    )

    results = await service.search_all("Python")

    assert results == stackoverflow


@pytest.mark.asyncio
async def test_all_sources_fail(monkeypatch):
    mock_provider(
        monkeypatch, "search_wikipedia",
        error=RuntimeError("Wikipedia unavailable"),
    )
    mock_provider(
        monkeypatch, "search_github",
        error=RuntimeError("GitHub unavailable"),
    )
    mock_provider(
        monkeypatch, "search_stackoverflow",
        error=RuntimeError("StackOverflow unavailable"),
    )

    with pytest.raises(SearchUnavailableError):
        await service.search_all("Python")


@pytest.mark.asyncio
async def test_all_sources_return_empty_lists(monkeypatch):
    mock_provider(monkeypatch, "search_wikipedia", results=[])
    mock_provider(monkeypatch, "search_github", results=[])
    mock_provider(monkeypatch, "search_stackoverflow", results=[])

    results = await service.search_all("something unknown")

    assert results == []


@pytest.mark.asyncio
async def test_one_source_fails_and_others_return_empty_lists(monkeypatch):
    mock_provider(
        monkeypatch, "search_wikipedia",
        error=RuntimeError("Wikipedia unavailable"),
    )
    mock_provider(monkeypatch, "search_github", results=[])
    mock_provider(monkeypatch, "search_stackoverflow", results=[])

    results = await service.search_all("something unknown")

    assert results == []


@pytest.mark.asyncio
async def test_search_all_passes_query_to_all_providers(monkeypatch):
    wiki_mock = AsyncMock(return_value=[])
    github_mock = AsyncMock(return_value=[])
    stackoverflow_mock = AsyncMock(return_value=[])

    monkeypatch.setattr(service, "search_wikipedia", wiki_mock)
    monkeypatch.setattr(service, "search_github", github_mock)
    monkeypatch.setattr(service, "search_stackoverflow", stackoverflow_mock)

    query = "Python asyncio"

    await service.search_all(query)

    wiki_mock.assert_awaited_once_with(query)
    github_mock.assert_awaited_once_with(query)
    stackoverflow_mock.assert_awaited_once_with(query)

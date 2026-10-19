import re

import json

import aiohttp
import pytest
from aioresponses import aioresponses

from bot.providers.github import search_github
from bot.providers.wikipedia import search_wikipedia
from bot.providers.stackoverflow import search_stackoverflow


GITHUB_URL = re.compile(
    r"https://api\.github\.com/search/repositories.*"
)
WIKIPEDIA_URL = re.compile(
    r"https://ru\.wikipedia\.org/w/api\.php.*"
)
STACKOVERFLOW_URL = re.compile(
    r"https://api\.stackexchange\.com/2\.3/search/advanced.*"
)


# ---------- GitHub ----------

@pytest.mark.asyncio
async def test_github_success():
    payload = {
        "items": [
            {
                "full_name": "python/cpython",
                "description": "Python programming language",
                "language": "Python",
                "stargazers_count": 100,
                "html_url": "https://github.com/python/cpython",
            }
        ]
    }

    with aioresponses() as mocked:
        mocked.get(GITHUB_URL, payload=payload)

        results = await search_github("python")

    assert len(results) == 1
    assert results[0].title == "python/cpython"
    assert results[0].source == "GitHub"
    assert results[0].language == "Python"
    assert results[0].stars == 100


@pytest.mark.asyncio
async def test_github_empty_results():
    with aioresponses() as mocked:
        mocked.get(GITHUB_URL, payload={"items": []})

        results = await search_github("query-with-no-results")

    assert results == []


@pytest.mark.asyncio
async def test_github_http_error():
    with aioresponses() as mocked:
        mocked.get(GITHUB_URL, status=500)

        with pytest.raises(aiohttp.ClientResponseError):
            await search_github("python")


@pytest.mark.asyncio
async def test_github_invalid_json():
    with aioresponses() as mocked:
        mocked.get(
            GITHUB_URL,
            body="{invalid json",
            content_type="application/json",
        )

        with pytest.raises(json.JSONDecodeError):
            await search_github("python")


# ---------- Wikipedia ----------

@pytest.mark.asyncio
async def test_wikipedia_success():
    payload = {
        "query": {
            "pages": [
                {
                    "title": "Python",
                    "description": "Programming language",
                    "fullurl": "https://ru.wikipedia.org/wiki/Python",
                }
            ]
        }
    }

    with aioresponses() as mocked:
        mocked.get(WIKIPEDIA_URL, payload=payload)

        results = await search_wikipedia("Python")

    assert len(results) == 1
    assert results[0].title == "Python"
    assert results[0].description == "Programming language"
    assert results[0].source == "Wikipedia"
    assert results[0].url == "https://ru.wikipedia.org/wiki/Python"


@pytest.mark.asyncio
async def test_wikipedia_empty_results():
    with aioresponses() as mocked:
        mocked.get(WIKIPEDIA_URL, payload={"query": {"pages": []}})

        results = await search_wikipedia("query-with-no-results")

    assert results == []


@pytest.mark.asyncio
async def test_wikipedia_http_error():
    with aioresponses() as mocked:
        mocked.get(WIKIPEDIA_URL, status=500)

        with pytest.raises(aiohttp.ClientResponseError):
            await search_wikipedia("Python")


@pytest.mark.asyncio
async def test_wikipedia_invalid_json():
    with aioresponses() as mocked:
        mocked.get(
            WIKIPEDIA_URL,
            body="{invalid json",
            content_type="application/json",
        )

        with pytest.raises(json.JSONDecodeError):
            await search_wikipedia("Python")


# ---------- StackOverflow ----------

@pytest.mark.asyncio
async def test_stackoverflow_success():
    payload = {
        "items": [
            {
                "title": "How to use asyncio?",
                "link": "https://stackoverflow.com/questions/123",
                "score": 42,
                "answer_count": 3,
                "is_answered": True,
            }
        ]
    }

    with aioresponses() as mocked:
        mocked.get(STACKOVERFLOW_URL, payload=payload)

        results = await search_stackoverflow("asyncio")

    assert len(results) == 1
    assert results[0].title == "How to use asyncio?"
    assert results[0].source == "StackOverflow"
    assert results[0].score == 42
    assert results[0].answers == 3
    assert results[0].status == "Есть принятый ответ"


@pytest.mark.asyncio
async def test_stackoverflow_empty_results():
    with aioresponses() as mocked:
        mocked.get(STACKOVERFLOW_URL, payload={"items": []})

        results = await search_stackoverflow("query-with-no-results")

    assert results == []


@pytest.mark.asyncio
async def test_stackoverflow_http_error():
    with aioresponses() as mocked:
        mocked.get(STACKOVERFLOW_URL, status=500)

        with pytest.raises(aiohttp.ClientResponseError):
            await search_stackoverflow("asyncio")


@pytest.mark.asyncio
async def test_stackoverflow_invalid_json():
    with aioresponses() as mocked:
        mocked.get(
            STACKOVERFLOW_URL,
            body="{invalid json",
            content_type="application/json",
        )

        with pytest.raises(json.JSONDecodeError):
            await search_stackoverflow("asyncio")

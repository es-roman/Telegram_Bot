import asyncio

import pytest

import bot.providers.github as github


@pytest.mark.asyncio
async def test_github_limits_concurrent_requests(monkeypatch):
    limit = 5
    semaphore = asyncio.Semaphore(limit)

    # Используем отдельный семафор для этого теста
    monkeypatch.setattr(github, "semaphore", semaphore)

    active = 0
    max_active = 0

    class FakeResponse:
        def raise_for_status(self):
            pass

        async def json(self):
            return {
                "items": [
                    {
                        "full_name": "test/repository",
                        "description": "Test repository",
                        "language": "Python",
                        "stargazers_count": 10,
                        "html_url": "https://github.com/test/repository",
                    }
                ]
            }

    class FakeRequest:
        async def __aenter__(self):
            nonlocal active, max_active

            active += 1
            max_active = max(max_active, active)

            # Имитируем ожидание ответа API
            await asyncio.sleep(0.05)

            return FakeResponse()

        async def __aexit__(self, exc_type, exc, tb):
            nonlocal active
            active -= 1

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def get(self, *args, **kwargs):
            return FakeRequest()

    monkeypatch.setattr(
        github.aiohttp,
        "ClientSession",
        FakeSession,
    )

    results = await asyncio.gather(
        *(github.search_github(f"query-{i}") for i in range(10))
    )

    assert max_active == limit
    assert active == 0
    assert len(results) == 10
    assert all(len(result) == 1 for result in results)
    assert all(result[0].title == "test/repository" for result in results)

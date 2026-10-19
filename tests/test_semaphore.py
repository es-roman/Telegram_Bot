import asyncio
import pytest


@pytest.mark.asyncio
async def test_semaphore_limits_concurrent_tasks():
    limit = 5
    semaphore = asyncio.Semaphore(limit)

    active = 0
    max_active = 0

    async def fake_request():
        nonlocal active, max_active

        async with semaphore:
            active += 1
            max_active = max(max_active, active)

            # Имитируем медленный HTTP-запрос
            await asyncio.sleep(0.1)

            active -= 1

    await asyncio.gather(
        *(fake_request() for _ in range(10))
    )

    assert max_active == limit
    assert active == 0

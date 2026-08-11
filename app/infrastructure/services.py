# app/infrastructure/services.py
import asyncio

from tenacity import retry, stop_after_attempt, wait_fixed

from app.application.interfaces import (
    FirstServiceProtocol,
    SecondServiceProtocol,
    ThirdServiceProtocol,
)


class FirstServiceMock(FirstServiceProtocol):
    @retry(
        reraise=True,
        stop=stop_after_attempt(2),
        wait=wait_fixed(0.5)
    )
    async def __call__(self, user_id: int) -> dict[str, str]:
        await asyncio.sleep(1.5)
        if user_id == 12:
            raise ValueError("First endpoint can't be reached now")
        return {"name": "Pedro"}


class SecondServiceMock(SecondServiceProtocol):
    @retry(
        reraise=True,
        stop=stop_after_attempt(2),
        wait=wait_fixed(0.5)
    )
    async def __call__(self, user_id: int) -> dict[str, int]:
        await asyncio.sleep(1)
        if user_id == 11:
            raise ValueError("Second endpoint can't be reached now")
        return {"spent": 17990}


class ThirdServiceMock(ThirdServiceProtocol):
    @retry(
        reraise=True,
        stop=stop_after_attempt(2),
        wait=wait_fixed(0.5)
    )
    async def __call__(self, user_id: int) -> dict[str, int]:
        await asyncio.sleep(2)
        if user_id == 10:
            raise ValueError("Third endpoint can't be reached now")
        return {"bonuses": 50}

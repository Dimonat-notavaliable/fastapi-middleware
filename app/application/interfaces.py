# app/application/interfaces.py
from typing import Protocol


class FirstServiceProtocol(Protocol):
    async def __call__(self, user_id: int) -> dict[str, str]: ...


class SecondServiceProtocol(Protocol):
    async def __call__(self, user_id: int) -> dict[str, int]: ...


class ThirdServiceProtocol(Protocol):
    async def __call__(self, user_id: int) -> dict[str, int]: ...

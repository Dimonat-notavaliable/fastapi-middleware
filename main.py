# main.py
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed

from logging_config import logger

app = FastAPI()


class User(BaseModel):
    name: str | None = None
    spent: int | None = None
    bonuses: int | None = None


class UserReport(User):
    errors: list[str] | None = None


@retry(
    reraise=True,
    stop=stop_after_attempt(2),
    wait=wait_fixed(0.5)
)
async def get_first_endpoint(user_id: int) -> dict[str, str]:
    await asyncio.sleep(1.5)
    if user_id == 12:
        raise ValueError("First endpoint can't be reached now")
    return {"name": "Pedro"}


@retry(
    reraise=True,
    stop=stop_after_attempt(2),
    wait=wait_fixed(0.5)
)
async def get_second_endpoint(user_id: int) -> dict[str, int]:
    await asyncio.sleep(1)
    if user_id == 11:
        raise ValueError("Second endpoint can't be reached now")
    return {"spent": 17990}


@retry(
    reraise=True,
    stop=stop_after_attempt(2),
    wait=wait_fixed(0.5)
)
async def get_third_endpoint(user_id: int) -> dict[str, int]:
    await asyncio.sleep(2)
    if user_id == 10:
        raise ValueError("Third endpoint can't be reached now")
    return {"bonuses": 50}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/report/{user_id}", response_model=UserReport)
async def read_user(user_id: int, q: str | None = None):
    logger.info(f"Trying to get report for user with id={user_id}")

    first_request = asyncio.wait_for(get_first_endpoint(user_id), timeout=4.0)
    second_request = asyncio.wait_for(get_second_endpoint(user_id), timeout=4.0)
    third_request = asyncio.wait_for(get_third_endpoint(user_id), timeout=4.0)

    result = await asyncio.gather(
        first_request,
        second_request,
        third_request,
        return_exceptions=True
    )

    errors_list = []

    user_object = {}
    for idx, res in enumerate(result):
        if isinstance(res, asyncio.TimeoutError):
            errors_list.append(f"Timeout error occured on endpoint {idx + 1}")
            logger.error(f"Timeout error occured on endpoint {idx + 1}")
            continue
        if isinstance(res, Exception):
            errors_list.append(f"({type(res).__name__}): {res!s}")
            logger.error(f"({type(res).__name__}): {res!s}")
            continue

        if idx == 0:
            user_object["name"] = res["name"]
        elif idx == 1:
            user_object["spent"] = res["spent"]
        elif idx == 2:
            user_object["bonuses"] = res["bonuses"]

    return UserReport(
        name=user_object.get("name"),
        spent=user_object.get("spent"),
        bonuses=user_object.get("bonuses"),
        errors=errors_list
    )

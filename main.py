# main.py
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str | None = None
    spent: int | None = None
    bonuses: int | None = None


class UserReport(User):
    errors: list[str] | None = None


async def get_first_endpoint(user_id: int) -> dict[str, str]:
    await asyncio.sleep(1.5)
    if user_id == 12:
        raise ValueError("First endpoint can't be reached now")
    return {"name": "Pedro"}


async def get_second_endpoint(user_id: int) -> dict[str, int]:
    await asyncio.sleep(1)
    if user_id == 11:
        raise ValueError("Second endpoint can't be reached now")
    return {"spent": 17990}


async def get_third_endpoint(user_id: int) -> dict[str, int]:
    await asyncio.sleep(3)
    if user_id == 10:
        raise ValueError("Third endpoint can't be reached now")
    return {"bonuses": 50}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/report/{user_id}", response_model=UserReport)
async def read_user(user_id: int, q: str | None = None):
    result = await asyncio.gather(
        get_first_endpoint(user_id),
        get_second_endpoint(user_id),
        get_third_endpoint(user_id),
        return_exceptions=True
    )

    errors_list = []

    user_object = {}
    for idx, res in enumerate(result):
        if isinstance(res, Exception):
            errors_list.append(str(res))
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

# app/presentation/schemas.py
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    name: str | None = Field(
        default=None,
        title="User name (Optional)",
        description="The full name of the user"
    )
    spent: int | None = Field(
        default=None,
        title="Spent (Optional)",
        description="The amount of money spent by user"
    )
    bonuses: int | None = Field(
        default=None,
        title="Bonuses (Optional)",
        description="The amount of bonuses on user's account"
    )


class UserReportResponse(UserResponse):
    errors: list[str] | None = Field(
        default=None,
        title="Errors (Optional)",
        description="List of errors occured during user report collection"
    )

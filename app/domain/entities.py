# app/domain/entities.py
from dataclasses import dataclass


@dataclass
class User:
    name: str | None = None
    spent: int | None = None
    bonuses: int | None = None


@dataclass
class UserReport(User):
    errors: list[str] | None = None

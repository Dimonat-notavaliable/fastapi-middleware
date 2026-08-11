# app/presentation/dependencies.py
from typing import Annotated

from fastapi import Depends

from app.application.interfaces import (
    FirstServiceProtocol,
    SecondServiceProtocol,
    ThirdServiceProtocol,
)
from app.application.use_cases import GetUserReportUseCase
from app.infrastructure.services import (
    FirstServiceMock,
    SecondServiceMock,
    ThirdServiceMock,
)


def get_first_service() -> FirstServiceProtocol:
    return FirstServiceMock()


def get_second_service() -> SecondServiceProtocol:
    return SecondServiceMock()


def get_third_service() -> ThirdServiceProtocol:
    return ThirdServiceMock()


def get_user_report_use_case(
    first_service: Annotated[FirstServiceProtocol, Depends(get_first_service)],
    second_service: Annotated[SecondServiceProtocol, Depends(get_second_service)],
    third_service: Annotated[ThirdServiceProtocol, Depends(get_third_service)],
    timeout: float = 4.0
) -> GetUserReportUseCase:
    return GetUserReportUseCase(
        first_service=first_service,
        second_service=second_service,
        third_service=third_service,
        timeout=timeout
    )

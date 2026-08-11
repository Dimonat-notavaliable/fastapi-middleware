# app/application/use_cases.py
import asyncio

from app.application.interfaces import FirstServiceProtocol, SecondServiceProtocol, ThirdServiceProtocol
from app.domain.entities import UserReport
from app.config.logging_config import logger


class GetUserReportUseCase:
    def __init__(
        self,
        first_service: FirstServiceProtocol,
        second_service: SecondServiceProtocol,
        third_service: ThirdServiceProtocol,
        timeout: float = 4.0
    ) -> None:
        self._first_service = first_service
        self._second_service = second_service
        self._third_service = third_service
        self._timeout = timeout

    async def get_user_report(self, user_id: int) -> UserReport:
        logger.info(f"Trying to get report for user with id={user_id}")

        first_request = asyncio.wait_for(self._first_service(user_id), timeout=self._timeout)
        second_request = asyncio.wait_for(self._second_service(user_id), timeout=self._timeout)
        third_request = asyncio.wait_for(self._third_service(user_id), timeout=self._timeout)

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
                service_name = ["first", "second", "third"][idx]
                errors_list.append(f"Timeout error occured on service {service_name}")
                logger.error(f"Timeout error occured on service {service_name}")
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

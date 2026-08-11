# app/presentation/routers.py
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.use_cases import GetUserReportUseCase
from app.config.logging_config import logger
from app.presentation.dependencies import get_user_report_use_case
from app.presentation.docs import user_report_docs
from app.presentation.mappers import user_report_mapper
from app.presentation.schemas import UserReportResponse

router = APIRouter()


@router.get("/report/{user_id}/", **user_report_docs)
@router.get("/report/{user_id}", include_in_schema=False)
async def read_user(
    user_id: int,
    use_case: Annotated[GetUserReportUseCase, Depends(get_user_report_use_case)],
) -> UserReportResponse:
    try:
        response_domain = await use_case.get_user_report(user_id)
        output = user_report_mapper(response_domain)

        return output
    except Exception:
        logger.error("An error occurred in the read_user_exception endpoint.")
        raise

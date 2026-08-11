# app/presentation/mappers.py
from app.domain.entities import UserReport
from app.presentation.schemas import UserReportResponse


def user_report_mapper(report: UserReport) -> UserReportResponse:
    return UserReportResponse(
        name=report.name,
        spent=report.spent,
        bonuses=report.bonuses,
        errors=report.errors
    )

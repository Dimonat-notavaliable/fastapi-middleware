# app/presentation/docs.py
from http import HTTPStatus

from app.presentation.schemas import UserReportResponse

# ENDPOINT DOCS
user_report_docs = {
    "summary": "Endpoint to get the details of the user by it's id.",
    "description": "Get the details of the user.",
    "response_description": "The response contains the details of the user.",
    "status_code": HTTPStatus.OK,
    "response_model": UserReportResponse,
    "include_in_schema": True,
}

"""Webapp schemas module."""

from project_name.webapp.schemas.auth_schemas import GoogleUserInfo
from project_name.webapp.schemas.auth_schemas import LoginResponse
from project_name.webapp.schemas.auth_schemas import SessionData
from project_name.webapp.schemas.auth_schemas import UserResponse
from project_name.webapp.schemas.common_schemas import ErrorResponse
from project_name.webapp.schemas.common_schemas import HealthResponse

__all__ = [
    "ErrorResponse",
    "GoogleUserInfo",
    "HealthResponse",
    "LoginResponse",
    "SessionData",
    "UserResponse",
]

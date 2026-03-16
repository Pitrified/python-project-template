"""Webapp schemas module - re-exported from fastapi_tools."""

from fastapi_tools.schemas.auth import GoogleUserInfo
from fastapi_tools.schemas.auth import LoginResponse
from fastapi_tools.schemas.auth import SessionData
from fastapi_tools.schemas.auth import UserResponse
from fastapi_tools.schemas.common import ErrorResponse
from fastapi_tools.schemas.common import HealthResponse

__all__ = [
    "ErrorResponse",
    "GoogleUserInfo",
    "HealthResponse",
    "LoginResponse",
    "SessionData",
    "UserResponse",
]

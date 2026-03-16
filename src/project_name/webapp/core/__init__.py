"""Webapp core module - re-exported from fastapi_tools."""

from fastapi_tools.dependencies import get_current_user
from fastapi_tools.exceptions import NotAuthenticatedException
from fastapi_tools.exceptions import NotAuthorizedException
from fastapi_tools.exceptions import RateLimitExceededException

__all__ = [
    "NotAuthenticatedException",
    "NotAuthorizedException",
    "RateLimitExceededException",
    "get_current_user",
]

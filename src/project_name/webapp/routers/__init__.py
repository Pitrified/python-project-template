"""Webapp routers module."""

from project_name.webapp.routers.auth_router import router as auth_router
from project_name.webapp.routers.health_router import router as health_router

__all__ = [
    "auth_router",
    "health_router",
]

"""FastAPI dependency injection functions - re-exported from fastapi_tools."""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from fastapi_tools.dependencies import get_current_session as get_current_session
from fastapi_tools.dependencies import get_current_user as get_current_user
from fastapi_tools.dependencies import get_db_session as get_db_session
from fastapi_tools.dependencies import get_optional_user as get_optional_user
from fastapi_tools.dependencies import get_session_store as get_session_store

from project_name.params.project_name_params import get_webapp_params

if TYPE_CHECKING:
    from project_name.config.webapp import WebappConfig


@lru_cache
def get_settings() -> WebappConfig:
    """Get webapp configuration settings.

    Returns:
        WebappConfig instance.
    """
    return get_webapp_params().to_config()

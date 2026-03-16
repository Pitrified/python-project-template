"""FastAPI application factory for project_name."""

from fastapi import FastAPI
from fastapi_tools import create_app

from project_name.params.project_name_params import get_project_name_paths
from project_name.params.project_name_params import get_webapp_params
from project_name.webapp.routers.pages_router import router as pages_router


def build_app() -> FastAPI:
    """Build the FastAPI application using fastapi-tools.

    Returns:
        Configured FastAPI application instance.
    """
    params = get_webapp_params()
    config = params.to_config()
    paths = get_project_name_paths()

    return create_app(
        config=config,
        extra_routers=[pages_router],
        static_dir=paths.static_fol,
        templates_dir=paths.templates_fol,
    )

"""Jinja2 template engine configuration.

Provides a configured ``Jinja2Templates`` instance used by page routes
to render HTML responses.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.templating import Jinja2Templates

from project_name.params.project_name_params import get_project_name_paths

if TYPE_CHECKING:
    from project_name.config.webapp import WebappConfig

# Resolve the templates directory from ProjectNamePaths (single source of truth)
templates = Jinja2Templates(directory=str(get_project_name_paths().templates_fol))


def configure_templates(config: WebappConfig) -> None:
    """Inject application-wide globals into the Jinja2 environment.

    Called once during ``create_app()`` after config is loaded.

    Args:
        config: Webapp configuration.
    """
    templates.env.globals.update(
        {
            "app_name": config.app_name,
            "app_version": config.app_version,
            "debug": config.debug,
        },
    )

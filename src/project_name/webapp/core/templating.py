"""Jinja2 template engine configuration.

Provides a configured ``Jinja2Templates`` instance used by page routes
to render HTML responses.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from starlette.templating import Jinja2Templates

if TYPE_CHECKING:
    from project_name.config.webapp import WebappConfig

# Resolve the templates directory relative to this file
_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

templates = Jinja2Templates(directory=str(_TEMPLATE_DIR))


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

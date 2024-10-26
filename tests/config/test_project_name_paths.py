"""Test the project_name paths."""

import pytest

from project_name.config.project_name_config import PROJECT_NAME_PATHS


def test_project_name_paths() -> None:
    """Test the project_name paths."""
    assert PROJECT_NAME_PATHS.src_fol.name == "project_name"
    assert PROJECT_NAME_PATHS.root_fol.name == "python_project_template"
    assert PROJECT_NAME_PATHS.data_fol.name == "data"

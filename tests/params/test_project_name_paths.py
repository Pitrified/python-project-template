"""Test the project_name paths."""

import tomllib

from project_name.params.project_name_params import get_project_name_paths


def test_project_name_paths() -> None:
    """Test the project_name paths.

    The root is checked by the pyproject.toml it holds, not by its folder name:
    a clone can be named anything, and a worktree checkout is named
    ``<repo>-<suffix>``.
    """
    project_name_paths = get_project_name_paths()
    assert project_name_paths.src_fol.name == "project_name"
    pyproject_path = project_name_paths.root_fol / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert pyproject["project"]["name"] == "project-name"
    assert project_name_paths.data_fol.name == "data"

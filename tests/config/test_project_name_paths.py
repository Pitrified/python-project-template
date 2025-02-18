"""Test the project_name paths."""


from project_name.config.project_name_config import get_project_name_paths


def test_project_name_paths() -> None:
    """Test the project_name paths."""
    project_name_paths = get_project_name_paths()
    assert project_name_paths.src_fol.name == "project_name"
    assert project_name_paths.root_fol.name == "python_project_template"
    assert project_name_paths.data_fol.name == "data"

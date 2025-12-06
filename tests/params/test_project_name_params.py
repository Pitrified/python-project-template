"""Test the ProjectNameParams class."""

from project_name.params.project_name_params import ProjectNameParams
from project_name.params.project_name_params import get_project_name_params
from project_name.params.project_name_paths import ProjectNamePaths
from project_name.params.sample_params import SampleParams


def test_project_name_params_singleton() -> None:
    """Test that ProjectNameParams is a singleton."""
    params1 = ProjectNameParams()
    params2 = ProjectNameParams()
    assert params1 is params2
    assert get_project_name_params() is params1


def test_project_name_params_init() -> None:
    """Test initialization of ProjectNameParams."""
    params = ProjectNameParams()
    assert isinstance(params.paths, ProjectNamePaths)
    assert isinstance(params.sample, SampleParams)


def test_project_name_params_str() -> None:
    """Test string representation."""
    params = ProjectNameParams()
    s = str(params)
    assert "ProjectNameParams:" in s
    assert "ProjectNamePaths:" in s
    assert "SampleParams:" in s

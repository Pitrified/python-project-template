"""ProjectName project params.

Parameters are actual value of the config.
"""

from loguru import logger as lg

from project_name.metaclasses.singleton import Singleton
from project_name.params.project_name_paths import ProjectNamePaths


class ProjectNameParams(metaclass=Singleton):
    """ProjectName project parameters."""

    def __init__(self) -> None:
        """Load the ProjectName params."""
        lg.info("Loading ProjectName params")
        self.paths = ProjectNamePaths()

    def __str__(self) -> str:
        """Return the string representation of the object."""
        s = "ProjectNameParams:"
        s += f"\n{self.paths}"
        return s

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return str(self)


def get_project_name_params() -> ProjectNameParams:
    """Get the project_name params."""
    return ProjectNameParams()


def get_project_name_paths() -> ProjectNamePaths:
    """Get the project_name paths."""
    return get_project_name_params().paths

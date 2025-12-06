"""ProjectName project configuration."""

from loguru import logger as lg

from project_name.config.project_name_paths import ProjectNamePaths
from project_name.metaclasses.singleton import Singleton


class ProjectNameConfig(metaclass=Singleton):
    """ProjectName project configuration."""

    def __init__(self) -> None:
        """Load the ProjectName config."""
        lg.info("Loading ProjectName config")
        self.paths = ProjectNamePaths()

    def __str__(self) -> str:
        """Return the string representation of the object."""
        s = "ProjectNameConfig:"
        s += f"\n{self.paths}"
        return s

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return str(self)


def get_project_name_config() -> ProjectNameConfig:
    """Get the project_name config."""
    return ProjectNameConfig()


def get_project_name_paths() -> ProjectNamePaths:
    """Get the project_name paths."""
    return get_project_name_config().paths

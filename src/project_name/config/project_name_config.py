"""ProjectName project configuration."""

from loguru import logger as lg

from project_name.config.project_name_paths import ProjectNamePaths
from project_name.config.singleton import Singleton


class ProjectNameConfig(metaclass=Singleton):
    """ProjectName project configuration."""

    def __init__(self) -> None:
        lg.info(f"Loading ProjectName config")
        self.paths = ProjectNamePaths()

    def __str__(self) -> str:
        s = "ProjectNameConfig:"
        s += f"\n{self.paths}"
        return s

    def __repr__(self) -> str:
        return str(self)


PROJECT_NAME_CONFIG = ProjectNameConfig()
PROJECT_NAME_PATHS = PROJECT_NAME_CONFIG.paths

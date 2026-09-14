import json
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

@dataclass
class Project:
    """ A data class representing a project """

    id: UUID
    name: str
    description: str
    root_dir: Path

class ProjectService:
    """ A service class for managing projects """
    def __init__(self):
        self.current_project: Project | None = None
        self.project_config_path: Path | None = None

    @staticmethod
    def load_config(config_path: Path):
        """Loads a project config file from default location"""

        with open(config_path, "r") as f:
            config = json.load(f)

        return config

    def open_project(self, root: Path) -> Project:
        """ Open a project from the root directory """

        config_file = root / ".pynest" / "project.json"
        if not config_file.exists():
            raise FileNotFoundError(config_file)

        config = self.load_config(config_path=config_file)

        project = Project(
            id=UUID(config["id"]),
            name=config["name"],
            description=config["description"],
            root_dir=Path(config["root_dir"]),
        )

        self.current_project = project
        self.project_config_path = config_file

        return project

    def close_project(self) -> None:
        """ Closes the current project """

        self.current_project = None
        self.project_config_path = None

    def rename_project(self, new_name: str) -> None:
        """ Renames a project """

        self.current_project.name = new_name
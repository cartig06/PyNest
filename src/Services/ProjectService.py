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
    def load_config(config_path: Path) -> dict:
        """Loads a project config file from default location"""

        with config_path.open("r") as f:
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

    def save_project(self) -> None:
        """ Saves the project properties back to config file"""

        if self.current_project is None:
            raise RuntimeError("No project opened")

        if self.project_config_path is None:
            config_path = (self.current_project.root_dir /
                                        ".pynest" /
                                        "project.json")
            config_path.parent.mkdir(parents=True, exist_ok=True)
            self.project_config_path = config_path
        else:
            config_path = self.project_config_path

        config = {
            "id": str(self.current_project.id),
            "name": self.current_project.name,
            "description": self.current_project.description,
            "root_dir": str(self.current_project.root_dir),
        }

        with config_path.open("w") as f:
            json.dump(config, f, indent=4)
            f.write("\n")

    def rename_project(self, new_name: str) -> None:
        """ Renames a project """

        if self.current_project is None:
            raise RuntimeError("No project opened")

        self.current_project.name = new_name
        self.save_project()


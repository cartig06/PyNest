from dataclasses import dataclass
from pathlib import Path

@dataclass
class File:
    """ A data class representing a file """

    name: str
    path: Path
    contents: str


class FileService:
    """ A class handling logic for interacting with files """

    def __init__(self):
        self.active_file: File | None = None

    def open_file(self, path: Path) -> File:
        """ Sets the active file """

        if not path.exists():
            raise FileNotFoundError("Given file does not exist")

        if not path.is_file():
            raise IsADirectoryError("Given path is not a file")

        file_contents = path.read_text(encoding="utf-8")
        file = File(name=path.name, path=path, contents=file_contents)

        self.active_file = file

        return file

    def close_file(self) -> None:
        """ Closes the active file """

        self.active_file = None

    def save_file(self) -> None:
        """ Saves the contents of the active file """

        if self.active_file is None:
            raise ValueError("No active file")

        if not self.active_file.path.exists():
            self.active_file.path.parent.mkdir(parents=True, exist_ok=True)
            self.active_file.path.touch()

        self.active_file.path.write_text(self.active_file.contents, encoding="utf-8")

    def rename_file(self, new_name: str) -> None:
        """ Renames the active file """

        if self.active_file is None:
            raise ValueError("No active file")

        old_path = self.active_file.path
        new_path = old_path.parent / new_name

        self.active_file.path.rename(new_path)

        self.active_file.name = new_name
        self.active_file.path = new_path

    def delete_file(self) -> None:
        """ Deletes the active file """

        if self.active_file is None:
            raise ValueError("No active file")

        if not self.active_file.path.exists():
            raise FileNotFoundError("Given file does not exist")

        self.active_file.path.unlink()


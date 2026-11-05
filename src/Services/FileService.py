from pathlib import Path
from Models.File import File

class FileService:
    """ A class handling logic for interacting with files """

    @staticmethod
    def open_file(path: Path) -> File:
        """ Loads a file from a given path """

        if not path.exists():
            raise FileNotFoundError("Given file does not exist")

        if not path.is_file():
            raise IsADirectoryError("Given path is not a file")

        file_contents = path.read_text(encoding="utf-8")
        file = File(name=path.name, path=path, contents=file_contents)

        return file

    @staticmethod
    def save_file(active_file: File) -> None:
        """ Saves the contents of a given file to disk """

        if not active_file.path.exists():
            active_file.path.parent.mkdir(parents=True, exist_ok=True)
            active_file.path.touch()

        active_file.path.write_text(active_file.contents, encoding="utf-8")

    @staticmethod
    def rename_file(active_file: File, new_name: str) -> None:
        """ Renames a given file to a given name """

        old_path = active_file.path
        new_path = old_path.parent / new_name

        if new_path == old_path:
            return

        if new_path.exists():
            raise FileExistsError("Given file already exists")

        active_file.path.rename(new_path)

        active_file.name = new_name
        active_file.path = new_path

    @staticmethod
    def delete_file(active_file: File) -> None:
        """ Deletes a given file """

        if not active_file.path.exists():
            raise FileNotFoundError("Given file does not exist")

        active_file.path.unlink()

    @staticmethod
    def move_file(active_file: File, new_path_parent: Path) -> None:
        """ Moves a given file to a new directory """

        new_path = new_path_parent / active_file.path.name

        if new_path.exists():
            raise FileExistsError("Given file already exists")

        active_file.path.rename(new_path)
        active_file.path = new_path


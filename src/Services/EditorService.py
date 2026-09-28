from dataclasses import dataclass
from src.Services.FileService import FileService, File
from pathlib import Path

@dataclass
class EditorState:
    """ A data class containing information about the state of the editor """

    cursor_position: int = 0
    selection_start: int | None = None
    selection_end: int | None = None
    dirty: bool = False

    def reset(self) -> None:
        """ A method used to reset the editor's state """
        self.cursor_position = 0
        self.selection_start = None
        self.selection_end = None
        self.dirty = False

class EditorService:
    """ A service class handling logic for the editor frontend """

    def __init__(self, file_service: FileService, state: EditorState):
        self.file_service = file_service
        self.state = state

    @property
    def contents(self) -> str:
        """ Property referencing the contents of the active file """

        if self.file_service.active_file is None:
            raise ValueError("No active file")

        return self.file_service.active_file.contents

    @property
    def selected_text(self) -> str:
        if self.state.selection_start is None or self.state.selection_end is None:
            return ""

        return self.contents[self.state.selection_start : self.state.selection_end]

    def open(self, path: Path) -> File:
        """ A method allowing the editor to reset and open a file """

        opened_file = self.file_service.open_file(path)
        self.state.reset()
        return opened_file

    def close(self) -> None:
        """ A method to reset the editor and close the active file"""

        self.file_service.close_file()
        self.state.reset()

    def insert(self, to_insert: str) -> None:
        """ A method to insert text either into a selected block, or appending at the given position """

        contents = self.contents
        selection_start = self.state.selection_start
        selection_end = self.state.selection_end

        if selection_start is not None and selection_end is not None:
            contents = contents[:selection_start] + to_insert + contents[selection_end:]

            self.state.cursor_position = selection_start + len(to_insert)
            self.state.selection_start = None
            self.state.selection_end = None

        else:
            position = self.state.cursor_position
            contents = contents[:position] + to_insert + contents[position:]
            self.state.cursor_position = position + len(to_insert)

        self.file_service.active_file.contents = contents
        self.state.dirty = True

    def delete(self):
        """ A method to delete either a block of text or removing one character at the cursor"""

        contents = self.contents
        selection_start = self.state.selection_start
        selection_end = self.state.selection_end

        if selection_start is not None and selection_end is not None:
            contents = contents[:selection_start] + contents[selection_end:]
            self.state.cursor_position = selection_start
            self.state.selection_start = None
            self.state.selection_end = None

        else:
            if self.state.cursor_position >= len(contents):
                return

            contents = contents[:self.state.cursor_position] + contents[self.state.cursor_position + 1:]

        self.file_service.active_file.contents = contents
        self.state.dirty = True

    def backspace(self):
        """ A method allowing the editor to 'backspace' a character at the cursor position """

        if self.state.selection_start is not None and self.state.selection_end is not None:
            self.delete()
            return

        if self.state.cursor_position == 0:
            return

        contents = self.contents

        contents = contents[:self.state.cursor_position-1] + contents[self.state.cursor_position:]
        self.file_service.active_file.contents = contents
        self.state.cursor_position -= 1

        self.state.dirty = True

    def save(self):
        """ A method allowing the editor to save the contents of the active file """

        self.file_service.save_file()
        self.state.dirty = False

    def select(self, selection_start: int, selection_end: int) -> None:
        """ A method to select a block of text supplied with a start and end position """

        if self.file_service.active_file is None:
            raise RuntimeError("No active file")

        start = min(selection_start, selection_end)
        end = max(selection_start, selection_end)

        self.state.selection_start = start
        self.state.selection_end = end

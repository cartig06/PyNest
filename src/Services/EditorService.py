from dataclasses import dataclass
from Services.FileService import FileService, File
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
        self._clipboard = ""

    @property
    def contents(self) -> str:
        """ Property referencing the contents of the active file """

        if self.file_service.active_file is None:
            raise ValueError("No active file")

        return self.file_service.active_file.contents

    @property
    def cursor_line(self) -> int:
        """ Property referencing the active line number """

        return self.contents.count("\n",0, self.state.cursor_position)

    @property
    def cursor_column(self) -> int:
        """ Property referencing the active column number """

        position = self.state.cursor_position
        line_start = self.contents.rfind("\n", 0, position)

        if line_start == -1:
            return position
        else:
            return position - line_start - 1

    @property
    def cursor_line_column(self) -> tuple[int, int]:
        """ Property referencing the active line and column number """
        return self.cursor_line, self.cursor_column

    @property
    def selected_text(self) -> str:
        """ Property referencing the selected text """
        
        selection = self.selection_range()
        if selection is None:
            return ""

        start, end = selection

        return self.contents[start : end]

    @property
    def clipboard(self):
        """ Return the contents of the clipboard """

        return self._clipboard

    def open(self, path: Path) -> File:
        """ A method allowing the editor to reset and open a file """

        opened_file = self.file_service.open_file(path)
        self.state.reset()
        return opened_file

    def close(self) -> None:
        """ A method to reset the editor and close the active file"""

        self.file_service.close_file()
        self.state.reset()

    def move_cursor(self, position: int, is_selecting: bool) -> None:
        """ Moves the cursor to a given position while also handling selection"""

        # Clamp position value between zero and len(self.contents), making sure the value falls
        # between the two
        position = max(0, min(len(self.contents), position))

        if is_selecting:
            if self.state.selection_start is None:
                self.state.selection_start = self.state.cursor_position

            self.state.selection_end = position

        else:
            self.state.selection_start = None
            self.state.selection_end = None

        self.state.cursor_position = position

    def get_current_line(self):
        """ Returns the contents of the current line"""

        line = self.cursor_line
        lines = self.contents.splitlines(keepends=True)

        return lines[line] if line < len(lines) else ""

    def position_from_line_column(self, line: int, column: int) -> int:
        """ Returns a position from a given line and column number """

        if not self.contents:
            return 0

        lines = self.contents.splitlines(keepends=True)

        line_no = max(0, min(len(lines) - 1, line))
        line_start = sum(len(lines[i]) for i in range(line_no))

        line_length = len(lines[line_no].rstrip("\n"))

        column = max(0, min(line_length, column))

        return line_start + column

    def visual_cursor_column(self) -> int:
        """ Returns the current visual cursor column number accounting for tabs/escape sequences """

        line, column = self.cursor_line_column

        lines = self.contents.splitlines(keepends=True)
        if line >= len(lines):
            return column

        line_content = lines[line]
        return len(line_content[:column].expandtabs(4))

    def visual_position_from_line_column(self, line: int, visual_column: int) -> int:
        """ Returns a visual cursor position from a given row and visual column number, accounting for tabs """

        tab_size = 4   # How many spaces for tab
        lines = self.contents.splitlines(keepends=True)

        line = max(0, min(len(lines) - 1, line))
        content = lines[line].rstrip("\n")

        visual_position = 0

        for idx, char in enumerate(content):
            if char == "\t":
                tab_align = (visual_position // tab_size + 1) * tab_size

                if tab_align > visual_column:
                    return self.position_from_line_column(line, idx)

                visual_position = tab_align

            else:
                if visual_position >= visual_column:
                    return self.position_from_line_column(line, idx)

                visual_position += 1

        return self.position_from_line_column(line, len(content))


    def selection_range(self) -> tuple[int, int] | None:
        """ Normalizes a selection range."""

        if self.state.selection_start is None or self.state.selection_end is None:
            return None

        start = min(self.state.selection_start, self.state.selection_end)
        end = max(self.state.selection_start, self.state.selection_end)

        return start, end

    """ Methods to move the cursor via arrow keys"""
    def move_cursor_up(self, is_selecting: bool) -> None:
        # Moves the cursor up
        line = self.cursor_line

        column = self.visual_cursor_column()

        if line == 0:
            return

        line -= 1

        position = self.visual_position_from_line_column(line, column)
        self.move_cursor(position, is_selecting)


    def move_cursor_down(self, is_selecting: bool) -> None:
        # Moves the cursor down
        line = self.cursor_line
        column = self.visual_cursor_column()

        if line >= self.contents.count("\n"):
            return

        line += 1

        position = self.visual_position_from_line_column(line, column)
        self.move_cursor(position, is_selecting)

    def move_cursor_left(self, is_selecting: bool) -> None:
        # Moves the cursor left

        position = self.state.cursor_position - 1
        self.move_cursor(position, is_selecting)

    def move_cursor_right(self, is_selecting: bool) -> None:
        # Moves the cursor right

        position = self.state.cursor_position + 1
        self.move_cursor(position, is_selecting)

    def insert(self, to_insert: str) -> None:
        """ A method to insert text either into a selected block, or appending at the given position """

        contents = self.contents
        selection = self.selection_range()

        if selection is not None:
            start, end = selection

            contents = contents[:start] + to_insert + contents[end:]

            self.state.cursor_position = start + len(to_insert)
            self.state.selection_start = None
            self.state.selection_end = None

        else:
            position = self.state.cursor_position
            contents = contents[:position] + to_insert + contents[position:]
            self.state.cursor_position = position + len(to_insert)

        self.file_service.active_file.contents = contents
        self.state.dirty = True

    def get_indentation(self, line:str) -> str:
        """ Returns the indentation characters of a given line"""

        indentation = ""

        for char in line:
            if char in ("\t", " "):
                indentation += char
            else:
                break

        return indentation

    def indent(self):
        """ A method to indent text """

        line, column = self.cursor_line_column
        current_line = self.get_current_line()
        indentation = self.get_indentation(current_line)

        if self.should_add_indent(current_line[:column].rstrip()):
            indentation += "\t"

        self.insert("\n" + indentation)

    @staticmethod
    def should_add_indent(line:str) -> bool:
        """ Checks if editor add more indentation on newline"""

        stripped = line.strip()
        return stripped.endswith(":")


    def delete(self):
        """ A method to delete either a block of text or removing one character at the cursor"""

        contents = self.contents
        selection = self.selection_range()

        if selection is not None:
            start, end = selection

            contents = contents[:start] + contents[end:]
            self.state.cursor_position = start
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

        self.state.selection_start = selection_start
        self.state.selection_end = selection_end

    def copy(self) -> None:
        """ Copies the selected text to clipboard """

        self._clipboard = self.selected_text

    def paste(self):
        """ Pastes the contents of the clipboard """

        if not self.clipboard:
            return

        self.insert(self.clipboard)

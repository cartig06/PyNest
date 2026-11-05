from dataclasses import dataclass

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
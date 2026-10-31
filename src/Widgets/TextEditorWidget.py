from Services.EditorService import EditorService
from Widgets.CursorWidget import CursorWidget
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.StatusBar import StatusBar
from textual.widget import Widget
from textual.widgets import Static
from textual.message import Message
from rich.text import Text

class TextEditorWidget(Widget):
    """ Text editor Textual widget for displaying contents of the file """       # MAY NEED UPDATE LATER

    # CursorMoved message to better work with other classes
    class CursorMoved(Message):
        pass

    # A message to toggle help visibility
    class HelpVisibilityChanged(Message):
        pass

    # Bindings for textual
    BINDINGS = [
        # Movement
        ("up", "cursor_up", "Moves cursor up"),
        ("down", "cursor_down", "Moves cursor down"),
        ("left", "cursor_left", "Moves cursor left"),
        ("right", "cursor_right", "Moves cursor right"),

        #Help
        ("f1", "toggle_help", "Toggles help menu"),

        # Selection
        ("f2", "toggle_select", "Toggles select mode for movement"),

        # File Management
        ("ctrl+s", "save", "Save the active file"),

        # Clipboard
        ("f3", "copy", "Copy the selected text to clipboard"),
        ("f4", "paste", "Paste text from clipboard"),

    ]

    AUTO_CLOSE = {
        "(": ")",
        "[": "]",
        "{": "}",
        '"': '"',
        "'": "'",
    }

    def __init__(self, editor_service: EditorService):
        super().__init__()
        self.editor_service = editor_service
        self.can_focus = True
        self.select_mode = False

    @property
    def cursor_line(self) -> int:
        return self.editor_service.cursor_line

    def on_mount(self) -> None:
        self.refresh_editor()

    def update_cursor(self):
        """ Updates cursor widget position """

        line = self.editor_service.cursor_line
        column = self.editor_service.visual_cursor_column()

        cursor = self.query_one("#cursor", CursorWidget)
        cursor.styles.offset = (column, line)
        cursor.pause_blink()

    def refresh_editor(self):
        """ Refreshes editor contents """

        contents = self.editor_service.contents.expandtabs(4)
        line_count = self.app.query_one("#lines", LineNumbersWidget)
        status = self.app.query_one("#status", StatusBar)

        start = self.editor_service.state.selection_start
        end = self.editor_service.state.selection_end

        rendered_text = Text(contents)

        if start is not None and end is not None:
            selection_start = self.editor_service.visual_position_from_logical(min(start, end))
            selection_end = self.editor_service.visual_position_from_logical(max(start, end))
            rendered_text.stylize("on #3a3d41", selection_start, selection_end)

        text = self.query_one("#text", Static)


        text.update(rendered_text)
        line_count.refresh_line_count()

        self.post_message(self.CursorMoved())

        status.update_info(
            self.select_mode,
            self.editor_service.file_service.active_file.name,
            self.editor_service.cursor_line,
            self.editor_service.visual_cursor_column(),
            self.editor_service.state.dirty
        )


        self.update_cursor()

    def action_toggle_help(self):
        """ Toggles help menu """
        self.post_message(self.HelpVisibilityChanged())

    def stop_selecting(self) -> None:
        """ Moves back into insert mode after performing selection operations """
        self.select_mode = False
        self.editor_service.state.selection_start = None
        self.editor_service.state.selection_end = None

    def action_cursor_right(self) -> None:
        """ Moves cursor right in editor """

        self.editor_service.move_cursor_right(self.select_mode)
        self.refresh_editor()

    def action_cursor_left(self) -> None:
        """ Moves cursor left in editor """

        self.editor_service.move_cursor_left(self.select_mode)
        self.refresh_editor()

    def action_cursor_up(self) -> None:
        """ Moves cursor up in editor """

        self.editor_service.move_cursor_up(self.select_mode)
        self.refresh_editor()

    def action_cursor_down(self) -> None:
        """ Moves cursor down in editor """

        self.editor_service.move_cursor_down(self.select_mode)
        self.refresh_editor()

    def action_toggle_select(self) -> None:
        """ Toggles select mode """

        self.select_mode = not self.select_mode
        self.refresh_editor()

    def action_copy(self) -> None:
        """ Copies selected text to clipboard """

        self.editor_service.copy()

    def action_paste(self) -> None:
        """ Pastes text from clipboard """
        if self.editor_service.clipboard is None:
            return

        self.editor_service.paste()
        self.stop_selecting()
        self.refresh_editor()

    def action_save(self) -> None:
        """ Saves the current file """

        self.notify(f"File: {self.editor_service.file_service.active_file.name} has been saved.")
        self.editor_service.save()
        self.refresh_editor()

    def on_key(self, event):
        # Backspace
        if event.key == "backspace":
            self.editor_service.backspace()
            self.stop_selecting()
            self.refresh_editor()
            event.prevent_default()

        # Forward delete
        elif event.key == "delete":
            self.editor_service.delete()
            self.stop_selecting()
            self.refresh_editor()
            event.prevent_default()

        # New line
        elif event.key == "enter":
            self.editor_service.indent()
            self.stop_selecting()
            self.refresh_editor()
            event.prevent_default()

        # Tab
        elif event.key == "tab":
            self.editor_service.insert("\t")
            self.stop_selecting()
            self.refresh_editor()
            event.prevent_default()


        # Insertion
        elif event.character and event.character.isprintable():
            # Auto-Close characters
            if event.character in self.AUTO_CLOSE:
                self.editor_service.insert(event.character)
                self.editor_service.insert(self.AUTO_CLOSE[event.character])
                self.editor_service.move_cursor_left(False)

            # Default text insertion
            else:
                self.editor_service.insert(event.character)

            self.stop_selecting()
            self.refresh_editor()
            event.prevent_default()


    def compose(self):
        contents = self.editor_service.contents.expandtabs(4)
        yield Static(contents, id="text")
        yield CursorWidget()
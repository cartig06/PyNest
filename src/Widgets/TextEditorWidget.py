from Services.EditorService import EditorService
from Widgets.CursorWidget import CursorWidget
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.StatusBar import StatusBar
from textual.widget import Widget
from textual.widgets import Static

class TextEditorWidget(Widget):
    """ Text editor Textual widget for displaying contents of the file """       # MAY NEED UPDATE LATER

    # Bindings for textual
    BINDINGS = [
        # Movement
        ("up", "cursor_up", "Moves cursor up"),
        ("down", "cursor_down", "Moves cursor down"),
        ("left", "cursor_left", "Moves cursor left"),
        ("right", "cursor_right", "Moves cursor right"),

        # Selection
        ("f2", "toggle_select", "Toggles select mode for movement"),

        # File Management
        ("ctrl+s", "save", "Save the active file"),

        # Clipboard
        ("ctrl+shift+c", "copy", "Copy the selected text to clipboard"),
        ("ctrl+shift+v", "paste", "Paste text from clipboard"),

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

    def on_mount(self) -> None:
        self.refresh_editor()

    def update_cursor(self):
        """ Updates cursor widget position """

        line, _ = self.editor_service.cursor_line_column
        column = self.editor_service.visual_cursor_column()

        cursor = self.query_one("#cursor", CursorWidget)
        cursor.styles.offset = (column, line)
        cursor.pause_blink()

    def refresh_editor(self):
        """ Refreshes editor contents """

        contents = self.editor_service.contents.expandtabs(4)
        line_count = self.app.query_one("#lines", LineNumbersWidget)
        status = self.app.query_one("#status", StatusBar)
        text = self.query_one("#text", Static)

        text.update(contents)
        line_count.refresh_line_count()

        status.update_info(
            self.select_mode,
            self.editor_service.file_service.active_file.name,
            self.editor_service.cursor_line,
            self.editor_service.visual_cursor_column(),
            self.editor_service.state.dirty
        )


        self.update_cursor()

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

        self.editor_service.paste()
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
            self.refresh_editor()
            event.prevent_default()

        # Forward delete
        elif event.key == "delete":
            self.editor_service.delete()
            self.refresh_editor()
            event.prevent_default()

        # New line
        elif event.key == "enter":
            self.editor_service.indent()
            self.refresh_editor()
            event.prevent_default()

        # Tab
        elif event.key == "tab":
            self.editor_service.insert("\t")
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

            self.refresh_editor()
            event.prevent_default()

    def compose(self):
        contents = self.editor_service.contents.expandtabs(4)
        yield Static(contents, id="text")
        yield CursorWidget()
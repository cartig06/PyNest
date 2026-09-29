from Services.EditorService import EditorService
from Widgets.CursorWidget import CursorWidget
from textual.widget import Widget
from textual.widgets import Static
from textual.dom import NoMatches

class TextEditorWidget(Widget):
    """ Text editor Textual widget for displaying contents of the file """       # MAY NEED UPDATE LATER

    def __init__(self, editor_service: EditorService):
        super().__init__()
        self.editor_service = editor_service

    def update_cursor(self):
        line, column = self.editor_service.cursor_line_column
        cursor = self.query_one("#cursor", CursorWidget)
        cursor.styles.offset = (column, line)

    def compose(self):
        yield Static(self.editor_service.contents, id="text")
        yield CursorWidget(self.editor_service)
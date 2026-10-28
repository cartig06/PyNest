from textual.message import Message
from textual.widget import Widget
from textual.containers import Horizontal, ScrollableContainer
from Services.EditorService import EditorService
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.TextEditorWidget import TextEditorWidget
from Widgets.StatusBar import StatusBar
from Widgets.HelpWidget import HelpWidget


class EditorWidget(Widget):
    """ Widget to house the text editor portion of PyNest"""

    def __init__(self, editor_service: EditorService):
        super().__init__()
        self.editor_service = editor_service

    def on_mount(self) -> None:
        self.text_editor = self.query_one(TextEditorWidget)
        self.editor_scroll = self.query_one("#editor_scroll", ScrollableContainer)
        self.text_editor.focus()

    def on_help_visibility_changed(self, message: TextEditorWidget.HelpVisibilityChanged) -> None:
        help_widget = self.query_one(HelpWidget)
        help_widget.toggle_visibility()

    def on_text_editor_cursor_moved(self, message: TextEditorWidget.CursorMoved) -> None:
        self.auto_scroll()

    def auto_scroll(self) -> None:
        cursor_line = self.text_editor.cursor_line

        top = self.editor_scroll.scroll_y
        bottom = top + self.editor_scroll.size.height

        if cursor_line >= bottom:
            self.editor_scroll.scroll_y = cursor_line - self.editor_scroll.size.height + 1

        elif cursor_line < top:
            self.editor_scroll.scroll_y = cursor_line

    def compose(self):
        yield ScrollableContainer(
            Horizontal(
            LineNumbersWidget(editor_service=self.editor_service),
                TextEditorWidget(editor_service=self.editor_service)
            ), id="editor_scroll"
        )

        yield StatusBar(id="status")

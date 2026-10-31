from textual import on
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
        self.help_menu = self.query_one(HelpWidget)
        self.editor_scroll = self.query_one("#editor_scroll", ScrollableContainer)
        self.text_editor.focus()

    @on(TextEditorWidget.HelpVisibilityChanged)
    def on_text_editor_help_visibility_changed(
            self,
            message: TextEditorWidget.HelpVisibilityChanged
    ) -> None:
        """ Message handler for help menu visibility """
        self.help_menu.toggle_visibility()

    @on(TextEditorWidget.CursorMoved)
    def on_text_editor_cursor_moved(self, message: TextEditorWidget.CursorMoved) -> None:
        """ Message handler for auto scrolling functionality """
        self.auto_scroll()

    def auto_scroll(self) -> None:
        """ Automatically scrolls the cursor when needed upon cursor movement"""
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

        yield HelpWidget()
        yield StatusBar(id="status")

from textual import on
from textual.widget import Widget
from textual.containers import Horizontal, ScrollableContainer
from pathlib import Path
from uuid import UUID
from Models.Document import Document
from Services.FileService import FileService
from Services.EditorService import EditorService
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.TextEditorWidget import TextEditorWidget
from Widgets.StatusBar import StatusBar
from Widgets.HelpWidget import HelpWidget


class EditorWidget(Widget):
    """ Widget to house the text editor portion of PyNest"""

    def __init__(self, file_service: FileService):
        super().__init__()
        self.file_service = file_service
        self.documents = {}
        self.active_editor = None
        self.active_document = None
        self.active_container = None

    # Events
    def on_mount(self) -> None:
        self.help_menu = self.query_one(HelpWidget)
        self.editor_scroll = self.query_one("#editor_scroll", ScrollableContainer)
        if self.active_editor is not None:
            self.active_editor.focus()

    def on_click(self) -> None:
        if self.active_editor is not None:
            self.active_editor.focus()

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

        if self.active_editor is None:
            return

        cursor_line = self.active_editor.cursor_line

        top = self.editor_scroll.scroll_y
        bottom = top + self.editor_scroll.size.height

        if cursor_line >= bottom:
            self.editor_scroll.scroll_y = cursor_line - self.editor_scroll.size.height + 1

        elif cursor_line < top:
            self.editor_scroll.scroll_y = cursor_line


    # Editor Management
    def open_document(self, path: Path) -> None:
        """ Opens a document and creates an editor instance for it """

        file = self.file_service.open_file(path)
        document = Document(file)
        editor_service = EditorService(self.file_service, document)

        editor = TextEditorWidget(editor_service)
        line_numbers = LineNumbersWidget(editor_service=editor_service)

        editor_container = Horizontal(
            line_numbers,
            editor
        )

        editor_container.display = False

        self.documents[document.id] = {
            "document": document,
            "editor_service": editor_service,
            "editor": editor,
            "container": editor_container
        }

        self.editor_scroll.mount(editor_container)

        if self.active_document is None:
            self.switch_document(document.id)


    def close_document(self, id: UUID) -> None:
        """ Closes a document and removes the editor instance """

        if id not in self.documents:
            return

        data = self.documents[id]
        document = data["document"]
        container = data["container"]

        document_was_active = self.active_document is not None and self.active_document.id == document.id

        container.remove()
        del self.documents[id]

        if document_was_active:
            self.active_document = None
            self.active_editor = None
            self.active_container =None

            if self.documents:
                next_doc = next(iter(self.documents))
                self.switch_document(next_doc)

    def switch_document(self, id: UUID) -> None:
        """ Switches the focused editor to active document """

        if id not in self.documents:
            return

        if self.active_container is not None:
            self.active_container.display = False

        data = self.documents[id]

        self.active_document = data["document"]
        self.active_editor = data["editor"]
        self.active_container = data["container"]

        self.active_container.display = True
        self.active_editor.focus()

    def compose(self):
        yield ScrollableContainer(id="editor_scroll")

        yield HelpWidget()
        yield StatusBar(id="status")

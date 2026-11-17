from textual import on
from textual.widget import Widget
from textual.containers import Horizontal, ScrollableContainer, Vertical
from pathlib import Path
from uuid import UUID
from Models.Document import Document
from Services.FileService import FileService
from Services.EditorService import EditorService
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.TabsBarWidget import TabsBarWidget
from Widgets.TabWidget import TabWidget
from Widgets.TextEditorWidget import TextEditorWidget
from Widgets.StatusBar import StatusBar
from Widgets.HelpWidget import HelpWidget


class EditorWidget(Widget):
    """ Widget to house the text editor portion of PyNest"""

    def __init__(self, file_service: FileService):
        super().__init__()
        self.file_service = file_service
        self.documents = {}
        self.active_document = None

    @property
    def active_editor(self):
        if self.active_document is None:
            return None

        return self.documents[self.active_document.id]["editor"]

    @property
    def active_container(self):
        if self.active_document is None:
            return None

        return self.documents[self.active_document.id]["container"]

    # Events
    def on_mount(self) -> None:
        self.help_menu = self.query_one(HelpWidget)
        self.editor_scroll = self.query_one("#editor_scroll", ScrollableContainer)
        self.tabs_bar = self.query_one(TabsBarWidget)

        if self.active_editor is not None:
            self.active_editor.focus()

    def on_click(self) -> None:
        if self.active_editor is not None:
            self.active_editor.focus()

    @on(TabWidget.TabSelected)
    def on_tabs_bar_tab_selected(self, message: TabWidget.TabSelected) -> None:
        """ Message handler for tab selection """
        self.switch_document(message.document_id)

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

    @on(TextEditorWidget.TabNavigationRequested)
    def on_text_editor_tab_navigation_requested(self, message: TextEditorWidget.TabNavigationRequested) -> None:
        """ Message handler for tab navigation requested """

        current_document_ids = list(self.documents.keys())
        if len(current_document_ids) <= 1:
            return

        current_idx = current_document_ids.index(self.active_document.id)
        new_idx = (current_idx + message.direction) % len(current_document_ids)
        self.switch_document(current_document_ids[new_idx])

    @on(TextEditorWidget.CloseTabRequested)
    async def on_text_editor_close_tab_requested(self, message: TextEditorWidget.CloseTabRequested) -> None:
        """ Message handler for close tab requested """

        await self.close_document(self.active_document.id)

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
    async def open_document(self, path: Path) -> None:
        """ Opens a document and creates an editor instance for it """

        path = path.resolve()

        for document_id, data in self.documents.items():
            if data["document"].file.path.resolve() == path:
                self.switch_document(document_id)
                return

        file = self.file_service.open_file(path)
        document = Document(file)
        editor_service = EditorService(self.file_service, document)

        editor = TextEditorWidget(editor_service)
        line_numbers = LineNumbersWidget(editor_service=editor_service)

        editor_container = Horizontal(
            line_numbers,
            editor,
            id=f"editor_container_{document.id}",
        )

        editor_container.display = False

        self.documents[document.id] = {
            "document": document,
            "editor": editor,
            "container": editor_container
        }

        await self.editor_scroll.mount(editor_container)
        await self.tabs_bar.update_tabs()

        self.switch_document(document.id)


    async def close_document(self, id: UUID) -> None:
        """ Closes a document and removes the editor instance """

        if id not in self.documents:
            return

        data = self.documents[id]
        container = data["container"]

        document_was_active = self.active_document is not None and self.active_document.id == id

        container.remove()
        del self.documents[id]

        if document_was_active:
            self.active_document = None

            if self.documents:
                next_doc = next(iter(self.documents))
                self.switch_document(next_doc)
            else:
                self.query_one("#status", StatusBar).update_info(
                    False, "No document", 0, 0, False
                )

        await self.tabs_bar.update_tabs()

    async def close_documents_in_directory(self, deleted_path: Path):
        """ Closes documents contained in a deleted directory """
        deleted_path = deleted_path.resolve()

        for document_id, data in list(self.documents.items()):
            file_path = data["document"].file.path.resolve()

            if file_path == deleted_path or deleted_path in file_path.parents:
                await self.close_document(document_id)

    def switch_document(self, id: UUID) -> None:
        """ Switches the focused editor to active document """

        if id not in self.documents:
            return

        if self.active_container is not None:
            self.active_container.display = False

        data = self.documents[id]

        self.active_document = data["document"]

        self.tabs_bar.set_active_tab(self.active_document.id)
        self.active_container.display = True
        self.active_editor.refresh_editor()
        self.active_editor.focus()

    def compose(self):
        yield Vertical(
            TabsBarWidget(self.documents),
            ScrollableContainer(id="editor_scroll"),
            HelpWidget(),
            StatusBar(id="status"),
            id="editor_layout"
        )

from textual import on
from Services.FileService import FileService
from Services.ProjectService import ProjectService
from Widgets.EditorWidget import EditorWidget
from Widgets.FileExplorerWidget import FileExplorerWidget
from textual.containers import Horizontal
from textual.screen import Screen

class ProjectScreen(Screen):
    """ A class representing the workspace ("Project" screen) of PyNest """
    BINDINGS = [
        ("escape", "close_project", "Closes the current project"),
        ("ctrl+tab", "toggle_focus", "Toggles the selected widget"),
    ]

    def __init__(self, project_service: ProjectService, file_service: FileService):
        self.project_service = project_service
        self.file_service = file_service
        super().__init__()

    @on(FileExplorerWidget.FileDeleted)
    async def on_file_explorer_file_deleted(self, event: FileExplorerWidget.FileDeleted) -> None:
        """ File or folder is deleted """
        await self.query_one(EditorWidget).close_documents_in_directory(event.path)

    # Event handlers
    @on(FileExplorerWidget.FileSelected)
    async def on_file_explorer_file_selected(self, event: FileExplorerWidget.FileSelected):
        """ File from tree is selected """
        editor_widget = self.query_one(EditorWidget)
        await editor_widget.open_document(event.path)

    def action_close_project(self):
        """ Closes the current project and returns to welcome screen """
        self.app.notify("Closed Project")
        self.project_service.close_project()
        self.app.pop_screen()

    def action_toggle_focus(self):
        """ Toggles the focused widget """

        explorer = self.query_one(FileExplorerWidget)
        editor = self.query_one(EditorWidget)

        if explorer.has_focus:
            editor.active_editor.focus()
        else:
            explorer.focus()


    def compose(self):
        yield Horizontal(
            FileExplorerWidget(self.project_service),
            EditorWidget(self.file_service)
    )
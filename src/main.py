from tkinter.ttk import Style

from textual.app import App
from pathlib import Path
from Widgets.EditorWidget import EditorWidget
from Services.EditorService import EditorService, EditorState
from Services.FileService import FileService


class PyNestApp(App):
    CSS_PATH = "Style.css"

    def __init__(self, editor_service: EditorService):
        self.editor_service = editor_service
        super().__init__()


    def compose(self):
        yield EditorWidget(self.editor_service)

if __name__ == "__main__":
    editor_state = EditorState()
    file_service = FileService()
    editor_service = EditorService(file_service, editor_state)

    editor_service.open(Path(""))

    app = PyNestApp(editor_service)
    app.run()




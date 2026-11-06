from textual.app import App
from pathlib import Path
import sys
from Models.Document import Document
from Models.EditorState import EditorState
from Widgets.EditorWidget import EditorWidget
from Services.EditorService import EditorService
from Services.FileService import FileService


class PyNestApp(App):
    CSS_PATH = "Style.css"

    def __init__(self, editor_service: EditorService):
        self.editor_service = editor_service
        super().__init__()


    def compose(self):
        yield EditorWidget(self.editor_service)

def main():
    file_service = FileService()
    file = file_service.open_file(Path(sys.argv[1]))  # TEST PATH HERE
    document = Document(file)
    editor_service = EditorService(file_service, document)

    app = PyNestApp(editor_service)
    app.run()

if __name__ == "__main__":
    main()

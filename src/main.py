from typing import List
from textual.app import App
from pathlib import Path
import sys
from Widgets.EditorWidget import EditorWidget
from Services.FileService import FileService

class PyNestApp(App):
    CSS_PATH = "Style.css"

    def __init__(self, file_service: FileService, files: List[Path]):
        self.file_service = file_service
        self.files = files
        super().__init__()


    def compose(self):
        yield EditorWidget(self.file_service)

    async def on_mount(self):
        editor = self.query_one(EditorWidget)
        for file in self.files:
            await editor.open_document(file)

def main():
    file_service = FileService()
    paths = [Path(i) for i in sys.argv[1:]]

    app = PyNestApp(file_service, paths)
    app.run()

if __name__ == "__main__":
    main()

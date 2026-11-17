from Screens.WelcomeScreen import WelcomeScreen
from Services.ProjectService import ProjectService
from Services.FileService import FileService
import sys
from typing import List
from textual.app import App
from pathlib import Path

VERSION = "0.2.0" # Current Version. To be updated with releases

class PyNestApp(App):
    CSS_PATH = "Style.css"

    def __init__(self, file_service: FileService, project_service: ProjectService):
        self.file_service = file_service
        self.version = VERSION
        self.project_service = project_service
        super().__init__()


    def on_mount(self):
        self.push_screen(WelcomeScreen())

def main():
    file_service = FileService()
    project_service = ProjectService()

    app = PyNestApp(file_service, project_service)
    app.run()

if __name__ == "__main__":
    main()

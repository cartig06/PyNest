from Services.FileService import FileService
from Models.EditorState import EditorState

class Document:
    def __init__(self, file_service: FileService):
        self.file_service = file_service
        self.state = EditorState()


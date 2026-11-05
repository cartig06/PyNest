from Models.EditorState import EditorState
from Models.File import File

class Document:
    def __init__(self, file: File):
        self.file = file
        self.state = EditorState()


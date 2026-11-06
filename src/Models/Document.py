from Models.EditorState import EditorState
from Models.File import File
from uuid import uuid4

class Document:
    def __init__(self, file: File):
        self.id = uuid4()
        self.file = file
        self.state = EditorState()


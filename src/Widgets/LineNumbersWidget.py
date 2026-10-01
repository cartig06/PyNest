from textual.widgets import Static
from Services.EditorService import EditorService

class LineNumbersWidget(Static):
    """ A textual widget to display line numbers used in the text editor"""

    def __init__(self, editor_service: EditorService):
        super().__init__(id="lines")
        self.editor_service = editor_service

    def refresh_line_count(self):
        line_count = self.editor_service.contents.count("\n") + 1

        self.update("\n".join(str(number) for number in range(1, line_count + 1)))
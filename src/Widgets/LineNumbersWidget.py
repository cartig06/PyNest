from textual.widget import Widget
from Services.EditorService import EditorService

class LineNumbersWidget(Widget):
    """ A textual widget to display line numbers used in the text editor"""

    def __init__(self, editor_service: EditorService):
        super().__init__()
        self.editor_service = editor_service

    def render(self):
        line_count = self.editor_service.contents.count("\n") + 1

        return "\n".join(str(number) for number in range(1, line_count + 1))
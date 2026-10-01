from textual.widget import Widget
from textual.containers import Horizontal
from Services.EditorService import EditorService
from Widgets.LineNumbersWidget import LineNumbersWidget
from Widgets.TextEditorWidget import TextEditorWidget
from Widgets.StatusBar import StatusBar


class EditorWidget(Widget):
    """ Widget to house the text editor portion of PyNest"""

    def __init__(self, editor_service: EditorService):
        super().__init__()
        self.editor_service = editor_service

    def compose(self):
        yield Horizontal(
            LineNumbersWidget(editor_service=self.editor_service),
            TextEditorWidget(editor_service=self.editor_service)
        )
        yield StatusBar(id="status")

from textual.widget import Widget
from Services.EditorService import EditorService

class CursorWidget(Widget):
    def __init__(self, editor_service: EditorService):
        super().__init__(id="cursor")
        self.editor_service = editor_service
        self.on = True

    def on_mount(self):
        self.set_interval(0.5, self.toggle)

    def toggle(self):
        self.on = not self.on

        if self.on:
            self.styles.display="block"
        else:
            self.styles.display="none"

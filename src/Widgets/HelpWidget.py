from textual.widgets import Static
from textual.message import Message

class HelpWidget(Static):
    def __init__(self):
        super().__init__(
            "F1: Toggle Help  |  F2: Select Mode  |  "
            "Ctrl+S: Save  |  Ctrl+Shift+C: Copy  |  "
            "Ctrl+Shift+V: Paste",
            id="help",
        )

        self.display = False

    def toggle_visibility(self):
        self.display = not self.display
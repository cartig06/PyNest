from textual.widgets import Static
from textual.message import Message

class HelpWidget(Static):
    def __init__(self):
        super().__init__(
            "F1: Toggle Help  |  F2: Select Mode  |  "
            "F3: Copy  |  "
            "F4: Paste  |  Ctrl+S: Save",
            id="help",
        )

        self.display = True

    def toggle_visibility(self):
        self.display = not self.display
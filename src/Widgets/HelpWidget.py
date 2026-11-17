from textual.widgets import Static
from textual.message import Message

class HelpWidget(Static):
    def __init__(self):
        super().__init__(
            "Escape: Close project | Ctrl+Tab: Toggle Editor/Explorer\n\n"
            "Editor:\nF1: Toggle Help  |  F2: Select Mode  |  "
            "F3: Copy  |  "
            "F4: Paste  |  Ctrl+S: Save\n"
            "Home: Previous tab | End: Next tab | Ctrl+W: Close Tab\n\n"
            "File Tree:\nCtrl+D: Create Directory | Ctrl+F: Create File | Ctrl+X: Delete",
            id="help",
        )

        self.display = True

    def toggle_visibility(self):
        """ ... well, im sure you can guess """
        self.display = not self.display
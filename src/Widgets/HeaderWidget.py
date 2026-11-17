from textual.containers import Horizontal
from textual.widgets import Static
class HeaderWidget(Horizontal):
    """ Reusable header for various screens """

    def compose(self):
        yield Static(
                "[bold #3498FF]P[/][bold #FFC83D]N[/]",  # Yes, I used ChatGPT for text formatting
                classes="logo"
            )
        yield Static("PyNest", classes="app-name")
        yield Static(self.app.version, classes="version")
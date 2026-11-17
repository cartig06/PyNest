from Screens.CreateProjectScreen import CreateProjectScreen
from Screens.OpenProjectScreen import OpenProjectScreen
from Widgets.HeaderWidget import HeaderWidget
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button

class WelcomeScreen(Screen):
    """ A class representing the welcome screen to PyNest """

    BINDINGS = [
        ("o", "open_project", "Opens an existing project"),
        ("n", "create_project", "Creates a new project"),
        ("q", "quit", "Quits the application"),
    ]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """ Button pressed handler """

        if event.button.id == "open-project":
            self.action_open_project()

        elif event.button.id == "new-project":
            self.action_create_project()

    def action_open_project(self) -> None:
        """ If open project is selected """

        self.app.push_screen(
            OpenProjectScreen(self.app.project_service)
        )

    def action_create_project(self) -> None:
        """ If create project is selected """

        self.app.push_screen(
            CreateProjectScreen(self.app.project_service)
        )

    def action_quit(self) -> None:
        """ If quit is selected """

        self.app.exit()

    def compose(self):
        # Main container
        yield Vertical(
            # Header
            HeaderWidget(classes="header"),

            # Body
            Vertical(
                Static("Welcome to PyNest", classes="welcome-title"),
                Static("Let's make something awesome!", classes="welcome-subtitle"),
                Static(
                    "A lightweight, TUI Python IDE designed around your convenience.",
                    classes="welcome-description"
                ),
                classes="body"
            ),

            #Buttons
            Horizontal(
                Button("Open Project  [O]", id="open-project"),
                Button("New Project  [N]", id="new-project"),
                classes="actions"
            ),

            # Footer
            Static(
                "KEYBOARD SHORTCUTS     O  Open Project     N  New Project     Q  Quit",
                classes="footer"
            ),

            id="welcome"
        )
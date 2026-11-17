from pathlib import Path
from Widgets.HeaderWidget import HeaderWidget
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button


class CreateDirectoryScreen(Screen):
    """ A class representing the create directory screen. """

    BINDINGS = [
        ("escape", "go_back", "Go Back"),
    ]

    def __init__(self, directory: Path, on_created):
        super().__init__()
        self.directory = directory
        self.on_created = on_created

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            self.create_directory()
        else:
            self.app.pop_screen()

    def create_directory(self) -> None:
        """ Create a new directory using input """

        # Get Input
        name_input = self.query_one("#directory-name", Input)
        name = name_input.value.strip()

        if not name:
            self.app.notify("Project name is required.",
                            severity="error")
            return

        # Handle potential path traversal
        if Path(name).name != name:
            self.app.notify(
                "Please enter a valid directory name.",
                severity="error"
            )
            return

        directory_path = self.directory / name

        try:
            directory_path.mkdir(parents=True, exist_ok=False)

        # Exception checking
        except FileExistsError:
            self.app.notify("A directory with that name already exists.",
                            severity="error")
            return

        except OSError as error:
            self.app.notify(f"Could not create directory: {error}",
                            severity="error")
            return

        self.on_created()
        self.app.pop_screen()

    def action_go_back(self) -> None:
        """ Go back to project screen """
        self.app.pop_screen()

    def compose(self):
        yield HeaderWidget(classes="header")

        yield Vertical(
            Vertical(
                Static("Create a New Directory", classes="project-title"),

                Static(f"Adding to {self.directory}", classes="adding-to-path"),

                #Input
                Static("Directory Name", classes="directory-input-label"),
                Input(placeholder="Directory Name", id="directory-name"),

                #Buttons
                Horizontal(
                    Button("Create Directory", variant="primary", id="create"),
                    Button("Cancel", id="cancel"),
                    classes="project-actions"
                ),
                id="create-directory"
            ),
            classes="project-body"
        )

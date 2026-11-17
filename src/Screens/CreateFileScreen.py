from pathlib import Path
from Widgets.HeaderWidget import HeaderWidget
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button


class CreateFileScreen(Screen):
    """A class representing the create file screen """

    BINDINGS = [
        ("escape", "go_back", "Go Back"),
    ]

    def __init__(self, directory: Path, on_created):
        super().__init__()
        self.directory = directory
        self.on_created = on_created

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            self.create_file()
        else:
            self.app.pop_screen()

    def create_file(self) -> None:
        """Create a new file using the input."""

        name_input = self.query_one("#file-name", Input)
        name = name_input.value.strip()

        if not name:
            self.app.notify(
                "File name is required.",
                severity="error"
            )
            return

        if Path(name).name != name:
            self.app.notify(
                "Please enter a valid file name.",
                severity="error"
            )
            return

        file_path = self.directory / name

        try:
            file_path.touch(exist_ok=False)

        except FileExistsError:
            self.app.notify(
                "A file with that name already exists.",
                severity="error"
            )
            return

        except OSError as error:
            self.app.notify(
                f"Could not create file: {error}",
                severity="error"
            )
            return

        self.on_created()
        self.app.pop_screen()

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def compose(self):
        yield HeaderWidget(classes="header")

        yield Vertical(
            Vertical(
                Static("Create a New File", classes="project-title"),
                Static(f"Adding to {self.directory}", classes="adding-to-path"),

                Static("File Name", classes="directory-input-label"),
                Input(placeholder="File Name (e.g. main.py)", id="file-name"),

                Horizontal(
                    Button("Create File", variant="primary", id="create"),
                    Button("Cancel", id="cancel"),
                    classes="project-actions"
                ),
                id="create-file"
            ),
            classes="project-body"
        )
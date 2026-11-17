from Screens.ProjectScreen import ProjectScreen
from Services.ProjectService import ProjectService
from Widgets.HeaderWidget import HeaderWidget
from pathlib import Path
from textual.widgets import Button, Static, Input
from textual.screen import Screen
from textual.containers import Vertical, Horizontal

class OpenProjectScreen(Screen):
    """ A class representing the open project screen. Allows the user to select an existing project """
    BINDINGS = [
        ("escape", "go_back", "Go Back"),
    ]

    def __init__(self, project_service: ProjectService):
        super().__init__()
        self.project_service = project_service

    # EVENT HANDLERS
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "open":
            self.open_project()
        else:
            self.action_go_back()

    def action_go_back(self):
        """ Go back to the welcome screen """

        self.app.pop_screen()

    def open_project(self):
        """ Opens an existing project using input fields """

        # Get inputs
        name_input = self.query_one("#project-name", Input)
        location_input = self.query_one("#project-location", Input)

        name = name_input.value.strip()
        location = location_input.value.strip()

        if not name or not location:
            self.app.notify("Project name and location are required.",
                            severity="error")
            return

        project_path = Path(location).expanduser() / name

        try:
            project = self.project_service.open_project(project_path)

            self.app.notify(f"Opened project: {project.name}")

        # Exception checking, duh!
        except FileNotFoundError:
            self.app.notify("Project directory could not be found.", severity="error")
            return

        except ValueError as error:
            self.app.notify(str(error), severity="error")
            return

        except OSError as error:
            self.app.notify(f"Could not open project: {error}", severity="error")
            return

        # Open Project Screen
        self.app.switch_screen(
            ProjectScreen(self.app.project_service, self.app.file_service)
        )

    def compose(self):
        yield HeaderWidget(classes="header")

        yield Vertical(
            Vertical(
                Static("Open an Existing Project", classes="project-title"),
                Static("Configure your new PyNest workspace.", classes="project-subtitle"),

                # Inputs
                Static("Project Name", classes="project-input-label"),
                Input(placeholder="My Python Project", id="project-name"),

                Static("PyNest Projects Location", classes="project-input-label"),
                Input(
                    placeholder=f"{Path.home()}/Documents/PyNestProjects",
                    value=f"{Path.home()}/Documents/PyNestProjects",
                    id="project-location"
                ),

                # Buttons
                Horizontal(
                    Button("Open Project", variant="primary", id="open"),
                    Button("Cancel", id="cancel"),
                    classes="project-actions"
                ),
                id="open-project-button"
            ),
            classes="project-body"
        )
from pathlib import Path
from Screens.ProjectScreen import ProjectScreen
from Widgets.HeaderWidget import HeaderWidget
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button

class CreateProjectScreen(Screen):
    """ A class representing the create project screen. """

    BINDINGS = [
        ("escape", "go_back", "Go Back"),
    ]

    def __init__(self, project_service):
        super().__init__()
        self.project_service = project_service

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            self.create_project()
        else:
            self.app.pop_screen()

    def create_project(self) -> None:
        """ Create a new project using input fields """

        # Get Inputs
        name_input = self.query_one("#project-name", Input)
        description_input = self.query_one("#project-description", Input)
        location_input = self.query_one("#project-location", Input)

        name = name_input.value.strip()
        description = description_input.value.strip()
        location = location_input.value.strip()

        if not name or not location:
            self.app.notify("Project name and location are required.",
                            severity="error")
            return

        project_path = Path(location).expanduser() / name

        try:
            project = self.project_service.create_project(
                name=name,
                description=description,
                root_dir=project_path
            )

            self.app.notify(f"Created project: {project.name}")

        # Exception checking
        except FileExistsError:
            self.app.notify("A directory with that name already exists.",
                            severity="error")
            return

        except OSError as error:
            self.app.notify(f"Could not create project: {error}",
                            severity="error")
            return

        # Open Project Screen
        self.app.switch_screen(
            ProjectScreen(self.app.project_service, self.app.file_service)
        )

    def action_go_back(self) -> None:
        """ Go back to welcome screen """
        self.app.pop_screen()

    def compose(self):
        yield HeaderWidget(classes="header")

        yield Vertical(
            Vertical(
                Static("Create a New Project", classes="project-title"),
                Static("Configure your new PyNest workspace.", classes="project-subtitle"),


                #Inputs
                Static("Project Name", classes="project-input-label"),
                Input(placeholder="My Python Project", id="project-name"),

                Static("Description", classes="project-input-label"),
                Input(placeholder="A short description of your project...",
                    id="project-description"),

                Static("Location", classes="project-input-label"),
                Input(
                    placeholder=f"{Path.home()}/Documents/PyNestProjects",
                    value=f"{Path.home()}/Documents/PyNestProjects",
                    id="project-location"
                ),

                #Buttons
                Horizontal(
                    Button("Create Project", variant="primary", id="create"),
                    Button("Cancel", id="cancel"),
                    classes="project-actions"
                ),
                id="create-project"
            ),
            classes="project-body"
        )

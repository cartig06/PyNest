from Services.ProjectService import ProjectService
from Screens.CreateDirectoryScreen import CreateDirectoryScreen
from Screens.CreateFileScreen import CreateFileScreen
from textual.widgets import Tree
from textual.message import Message
from pathlib import Path
import shutil

class FileExplorerWidget(Tree):
    """ A message class to inform the screen of a file deletion """

    BINDINGS = [
        ("ctrl+d", "create_directory", "Creates a new directory"),
        ("ctrl+f", "create_file", "Creates a new file"),
        ("ctrl+x", "delete", "Deletes a selected file or directory")
    ]

    class FileDeleted(Message):
        def __init__(self, path: Path):
            super().__init__()
            self.path = path

    class FileSelected(Message):
        """ A message class to inform the editor when a file is selected. """
        def __init__(self, path: Path):
            super().__init__()
            self.path = path

    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
        self.populated = set()

        root = project_service.project_root
        super().__init__(
            label=f"📁 {root.name}",
            data=root
        )

    def on_mount(self):
        self.populate_tree(self.root)

    def populate_tree(self, node):
        """ Populates the tree with the contents of a given directory (node) """

        directory = node.data

        # Prevent duplicated items when expanding/collapsing directories
        if directory in self.populated:
            return
        self.populated.add(directory)

        for path in self.project_service.get_directory_contents(directory):
            if path.is_dir():
                child = node.add(
                    f"📁 {path.name}",
                    data=path,
                    allow_expand=True
                )

            else:
                node.add_leaf(
                    f"📄 {path.name}",
                    data=path
                )

    def get_target_directory(self) -> Path:
        """ Returns the directory to which a file/folder will be created """

        node = self.cursor_node

        if node is None:
            return self.project_service.current_project.root_dir

        path = Path(node.data)

        # If selected node is a directory, return selected directory
        if path.is_dir():
            return path

        # Otherwise, return parent directory of selected file
        return path.parent

    def action_create_directory(self):
        """ Creates a new directory at the selected location """

        path = self.get_target_directory()
        self.app.push_screen(CreateDirectoryScreen(path, self.rebuild))

    def action_create_file(self):
        """ Creates a new file at the selected location """

        path = self.get_target_directory()
        self.app.push_screen(CreateFileScreen(path, self.rebuild))

    def action_delete(self):
        """ Deletes a selected file or directory """

        node = self.cursor_node
        if node is None or node is self.root:
            return

        path = Path(node.data)

        try:
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)

            self.rebuild()
            self.post_message(self.FileDeleted(path))

            self.app.notify(f"Deleted: {path.name}")

        except OSError as error:
            self.app.notify(f"Could not delete: {error}", severity="error")


    def rebuild(self):
        """ Effectively a callback method for CreateDirectoryScreen """

        self.populated.clear()
        self.root.remove_children()
        self.populate_tree(self.root)

    def on_tree_node_expanded(self, event: Tree.NodeExpanded):
        """ Event handler for expanding a directory """

        # Populate expanded directory
        self.populate_tree(event.node)

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        path = event.node.data

        if path.is_file():
            self.post_message(self.FileSelected(path))
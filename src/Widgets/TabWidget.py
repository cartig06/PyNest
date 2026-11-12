from textual.widgets import Button
from textual.message import Message
from uuid import UUID

class TabWidget(Button):
    """ A widget class representing a selectable tab """

    class TabSelected(Message):
        """ A message that broadcasts when a tab is selected"""
        def __init__(self, document_id: UUID):
            super().__init__()
            self.document_id = document_id

    def __init__(self, document_id: UUID, name:str ):
        super().__init__(name, id=f"tab-{document_id}")
        self.document_id = document_id

    def on_click(self) -> None:
        self.post_message(self.TabSelected(self.document_id))

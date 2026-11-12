from textual.containers import Horizontal
from uuid import UUID
from Widgets.TabWidget import TabWidget

class TabsBarWidget(Horizontal):
    """ A widget class representing the tabs bar containing all active documents """
    def __init__(self, documents):
        super().__init__()
        self.active_document_id = None
        self.documents = documents
        self.tabs = {}

    async def update_tabs(self):
        """ Updates the tabs bar contents """
        await self.remove_children()
        self.tabs.clear()

        for document_id, data in self.documents.items():
            document = data['document']

            tab = TabWidget(document_id, document.file.name)
            tab.add_class("tab")

            if document_id == self.active_document_id:
                tab.add_class("active_tab")

            self.tabs[document_id] = tab

            await self.mount(tab)

    def set_active_tab(self, document_id: UUID):
        """ Sets the active tab without refreshing bar """
        self.active_document_id = document_id

        for tab_id, tab in self.tabs.items():
            tab.set_class(tab_id == document_id, "active_tab")





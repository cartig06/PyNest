from textual.widgets import Static

class StatusBar(Static):
    def update_info(self, select_mode: bool, file_name: str, line: int, column: int, dirty: bool) -> None:
        """ Updates status bar information """

        mode = "SELECTING" if select_mode else "NORMAL"

        self.update(f"{mode}    |    {file_name}    |    Ln {str(line+1)}     "
                    f"|    Col {str(column+1)}    |    {"Modified" if dirty else "Saved"}")

from pathlib import Path
from dataclasses import dataclass

@dataclass
class File:
    """ A data class representing a file """

    name: str
    path: Path
    contents: str
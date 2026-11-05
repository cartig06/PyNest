from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

@dataclass
class Project:
    """ A data class representing a project """

    id: UUID
    name: str
    description: str
    root_dir: Path
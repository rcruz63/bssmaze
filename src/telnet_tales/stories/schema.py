"""Esquema del archivo de historia (R2.1). Los modelos de nodo viven en `engine`."""

from typing import Literal

from pydantic import Field

from telnet_tales.engine.models import FrozenModel
from telnet_tales.engine.story_models import (
    Encounter,
    Exit,
    Requirement,
    Story,
    StoryNode,
)

__all__ = ["Encounter", "Exit", "Requirement", "Story", "StoryFile", "StoryNode"]


class StoryFile(FrozenModel):
    # `status: draft` marca contenido pendiente de revisión humana; no cambia las reglas.
    status: Literal["draft", "final"] = "final"
    start: str = Field(min_length=1)
    nodes: tuple[StoryNode, ...]
    encounters: tuple[Encounter, ...] = ()

    def to_story(self) -> Story:
        """Indexa por id; un id repetido lo detecta el cargador antes de llegar aquí."""
        return Story(
            start=self.start,
            nodes={node.id: node for node in self.nodes},
            encounters={encounter.id: encounter for encounter in self.encounters},
        )

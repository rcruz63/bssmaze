"""Interfaz del narrador y contexto acotado (R4.1, R4.2).

El narrador solo ve `NarrationContext`: no recibe `GameState`, banderas ocultas ni la historia.
"""

from typing import Protocol

from telnet_tales.engine.actions import GameEvent, ProposedAction
from telnet_tales.engine.models import FrozenModel

MAX_PLAYER_TEXT = 200  # Tope de entrada del jugador (R5.4), también para el parser offline.


class PublicStats(FrozenModel):
    hit_points: int
    max_hit_points: int
    wits: int
    brawn: int
    luck: int
    inventory: tuple[str, ...]


class NarrationContext(FrozenModel):
    node_title: str
    node_text: str
    visible_exits: tuple[str, ...]
    visible_items: tuple[str, ...]
    public_stats: PublicStats
    recent_events: tuple[GameEvent, ...] = ()


class NarratorProvider(Protocol):
    async def narrate(self, context: NarrationContext) -> str: ...

    async def interpret(self, text: str, context: NarrationContext) -> ProposedAction: ...

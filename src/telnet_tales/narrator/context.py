"""Construye el contexto acotado que ve el narrador a partir del estado (R4.2)."""

from telnet_tales.engine.actions import GameEvent
from telnet_tales.engine.models import GameState
from telnet_tales.engine.rules import visible_items
from telnet_tales.engine.story_models import Story
from telnet_tales.narrator.provider import NarrationContext, PublicStats

RECENT_EVENT_LIMIT = 3  # Pocos eventos bastan para narrar y mantienen el prompt pequeño.


def public_stats(state: GameState) -> PublicStats:
    player = state.player
    return PublicStats(
        hit_points=player.hit_points,
        max_hit_points=player.max_hit_points,
        wits=player.stats.wits,
        brawn=player.stats.brawn,
        luck=player.stats.luck,
        inventory=player.inventory,
    )


def build_context(
    state: GameState, story: Story, events: tuple[GameEvent, ...] = ()
) -> NarrationContext:
    """Copia solo título, texto, salidas, objetos visibles, ficha pública y últimos eventos."""
    node = story.nodes[state.node_id]
    return NarrationContext(
        node_title=node.title,
        node_text=node.text,
        visible_exits=tuple(exit_.label for exit_ in node.exits),
        visible_items=visible_items(state, node),
        public_stats=public_stats(state),
        recent_events=events[-RECENT_EVENT_LIMIT:],
    )

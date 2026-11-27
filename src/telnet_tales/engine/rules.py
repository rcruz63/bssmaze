"""Reglas puras: mover, mirar, coger e inventario (R1.5). Devuelven estado nuevo."""

from collections.abc import Callable

from telnet_tales.engine.actions import (
    ActionResult,
    GameEvent,
    ProposedAction,
    RejectionReason,
    reject,
)
from telnet_tales.engine.models import MAX_INVENTORY, GameState
from telnet_tales.engine.story_models import Exit, Requirement, Story, StoryNode

Handler = Callable[[GameState, ProposedAction, Story], tuple[GameState, ActionResult]]


def normalize(text: str) -> str:
    return "_".join(text.lower().split())


def taken_flag(item_id: str) -> str:
    # Un objeto recogido no reaparece en el nodo aunque el jugador lo gaste después.
    return f"taken:{item_id}"


def requirement_met(state: GameState, requirement: Requirement | None) -> bool:
    if requirement is None:
        return True
    if requirement.item is not None:
        return requirement.item in state.player.inventory
    stats = state.player.stats.model_dump()
    return bool(requirement.stat and stats[requirement.stat] >= requirement.minimum)


def visible_items(state: GameState, node: StoryNode) -> tuple[str, ...]:
    return tuple(item for item in node.items if taken_flag(item) not in state.flags)


def _accept(state: GameState, *events: GameEvent) -> tuple[GameState, ActionResult]:
    return state, ActionResult(ok=True, events=events)


def _find_exit(node: StoryNode, target: str) -> Exit | None:
    wanted = normalize(target)
    return next((e for e in node.exits if normalize(e.label) == wanted), None)


def _move(state: GameState, action: ProposedAction, story: Story) -> tuple[GameState, ActionResult]:
    node = story.nodes[state.node_id]
    chosen = _find_exit(node, action.target or "")
    if chosen is None:
        return state, reject(RejectionReason.NO_SUCH_EXIT, "No such way out.")
    if not requirement_met(state, chosen.requirement):
        return state, reject(RejectionReason.REQUIREMENT_NOT_MET, "Something blocks the way.")
    moved = state.model_copy(update={"node_id": chosen.target_id, "turn": state.turn + 1})
    return _accept(moved, GameEvent(kind="moved", detail=chosen.target_id))


def _take(state: GameState, action: ProposedAction, story: Story) -> tuple[GameState, ActionResult]:
    wanted = normalize(action.target or "")
    present = visible_items(state, story.nodes[state.node_id])
    if wanted not in present:
        return state, reject(RejectionReason.ITEM_NOT_HERE, "Nothing like that here.")
    if len(state.player.inventory) >= MAX_INVENTORY:
        return state, reject(RejectionReason.INVENTORY_FULL, "Your pack is full.")
    player = state.player.model_copy(update={"inventory": (*state.player.inventory, wanted)})
    flags = state.flags | {taken_flag(wanted)}
    taken = state.model_copy(update={"player": player, "flags": flags, "turn": state.turn + 1})
    return _accept(taken, GameEvent(kind="took", detail=wanted))


def _look(state: GameState, action: ProposedAction, story: Story) -> tuple[GameState, ActionResult]:
    return _accept(state, GameEvent(kind="looked", detail=state.node_id))


def _inventory(
    state: GameState, action: ProposedAction, story: Story
) -> tuple[GameState, ActionResult]:
    return _accept(state, GameEvent(kind="inventory", detail=",".join(state.player.inventory)))


def _session_only(
    state: GameState, action: ProposedAction, story: Story
) -> tuple[GameState, ActionResult]:
    # `help` y `quit` los atiende la sesión; el motor solo los acepta sin tocar el estado.
    return _accept(state, GameEvent(kind=action.action_type))


def _unavailable(
    state: GameState, action: ProposedAction, story: Story
) -> tuple[GameState, ActionResult]:
    # `use`, `attack` y `flee` llegan con el combate (tarea 10).
    return state, reject(RejectionReason.NOT_AVAILABLE, "You cannot do that yet.")


NEEDS_TARGET = frozenset({"move", "take"})

HANDLERS: dict[str, Handler] = {
    "move": _move,
    "take": _take,
    "look": _look,
    "inventory": _inventory,
    "help": _session_only,
    "quit": _session_only,
}


def apply_action(
    state: GameState, action: ProposedAction, story: Story
) -> tuple[GameState, ActionResult]:
    """Valida y aplica una acción; si se rechaza, el estado devuelto es el mismo (P3)."""
    if story.nodes[state.node_id].is_ending:
        return state, reject(RejectionReason.GAME_OVER, "The line is dead.")
    if action.action_type in NEEDS_TARGET and not action.target:
        return state, reject(RejectionReason.MISSING_TARGET, "Do that to what?")
    return HANDLERS.get(action.action_type, _unavailable)(state, action, story)

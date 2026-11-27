"""Intérprete de órdenes por palabras clave: sin red, sin azar (R4.5, R5)."""

from telnet_tales.engine.actions import ActionType, ProposedAction
from telnet_tales.engine.rules import normalize
from telnet_tales.narrator.provider import MAX_PLAYER_TEXT, NarrationContext

VERBS: dict[str, ActionType] = {
    "go": "move", "walk": "move", "move": "move", "head": "move",
    "look": "look", "l": "look", "examine": "look", "x": "look",
    "take": "take", "get": "take", "grab": "take", "pick": "take",
    "use": "use", "read": "use", "drink": "use",
    "attack": "attack", "hit": "attack", "fight": "attack", "kill": "attack", "strike": "attack",
    "flee": "flee", "run": "flee",
    "inventory": "inventory", "inv": "inventory", "i": "inventory",
    "help": "help", "?": "help",
    "quit": "quit", "bye": "quit", "logoff": "quit", "hangup": "quit",
}  # fmt: skip
DIRECTIONS = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
FILLER = frozenset({"the", "a", "an", "to", "at", "on"})
FALLBACK = ProposedAction(action_type="help")  # Lo desconocido se trata como texto, no como orden.


def clean_words(text: str) -> list[str]:
    """Recorta a 200 caracteres: el texto del jugador es dato acotado (R5.4)."""
    # "pick up" se reduce a "take" para que "up" siga siendo una dirección válida.
    return text[:MAX_PLAYER_TEXT].lower().replace("pick up", "take").split()


def match_choice(words: list[str], choices: tuple[str, ...]) -> str | None:
    """Elige la opción cuyo id coincide entero, por su última palabra o por una palabra suelta."""
    wanted = normalize(" ".join(words))
    exact = [c for c in choices if normalize(c) == wanted]
    partial = [c for c in choices if wanted and wanted in normalize(c).split("_")]
    found = exact or partial
    return found[0] if found else None


def resolve_exit(words: list[str], context: NarrationContext) -> str | None:
    expanded = [DIRECTIONS.get(word, word) for word in words]
    return match_choice(expanded, context.visible_exits)


def target_choices(verb: ActionType, context: NarrationContext) -> tuple[str, ...]:
    if verb == "take":
        return context.visible_items
    return context.public_stats.inventory


def resolve_target(verb: ActionType, words: list[str], context: NarrationContext) -> str | None:
    if verb == "move":
        return resolve_exit(words, context) or " ".join(words) or None
    if verb in ("take", "use"):
        return match_choice(words, target_choices(verb, context)) or " ".join(words) or None
    return " ".join(words)[:40] or None


def interpret_text(text: str, context: NarrationContext) -> ProposedAction:
    """Siempre devuelve una acción válida; la validación de reglas es del motor."""
    words = clean_words(text)
    if not words:
        return FALLBACK
    bare_exit = resolve_exit(words, context)
    if bare_exit is not None:
        return ProposedAction(action_type="move", target=bare_exit)
    verb = VERBS.get(words[0])
    if verb is None:
        return FALLBACK
    rest = [word for word in words[1:] if word not in FILLER]
    return ProposedAction(action_type=verb, target=resolve_target(verb, rest, context))

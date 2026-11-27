"""Narrador offline determinista: plantillas y parser, sin red ni claves (R4.5)."""

from telnet_tales.engine.actions import GameEvent, ProposedAction
from telnet_tales.narrator.parser import interpret_text
from telnet_tales.narrator.provider import NarrationContext

EVENT_TEMPLATES = {
    "moved": "You move on through the dark.",
    "took": "You take the {item}.",
    "inventory": "You carry: {item}.",
    "help": "The SysOp whispers: try go, look, take, inventory or quit.",
    "quit": "You reach for the hangup key.",
}


def item_name(item_id: str) -> str:
    return item_id.replace("_", " ")


def event_line(event: GameEvent) -> str | None:
    template = EVENT_TEMPLATES.get(event.kind)
    if template is None:
        return None
    names = ", ".join(map(item_name, filter(None, event.detail.split(",")))) or "nothing"
    return template.format(item=names)


def node_lines(context: NarrationContext) -> list[str]:
    exits = ", ".join(context.visible_exits) or "none"
    lines = [context.node_title, context.node_text.rstrip(), f"Exits: {exits}"]
    if context.visible_items:
        lines.append("You see: " + ", ".join(map(item_name, context.visible_items)))
    return lines


class OfflineNarrator:
    """Cumple `NarratorProvider`; es el único narrador de los tests y la red de seguridad."""

    async def narrate(self, context: NarrationContext) -> str:
        notes = [line for line in map(event_line, context.recent_events) if line]
        return "\n".join([*notes, *node_lines(context)])

    async def interpret(self, text: str, context: NarrationContext) -> ProposedAction:
        return interpret_text(text, context)

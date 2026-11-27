"""Acciones propuestas, lista blanca y rechazos tipados (R5.1, R5.2)."""

from enum import StrEnum
from typing import Literal, get_args

from pydantic import Field, ValidationError

from telnet_tales.engine.models import FrozenModel

ActionType = Literal["move", "look", "take", "use", "attack", "flee", "inventory", "help", "quit"]
ALLOWED_ACTIONS: frozenset[str] = frozenset(get_args(ActionType))
MAX_TARGET_LENGTH = 40  # El texto del jugador está acotado: un objetivo largo nunca es válido.


class ProposedAction(FrozenModel):
    # Esquema estricto (`extra="forbid"` heredado): el modelo de lenguaje no puede añadir campos.
    action_type: ActionType
    target: str | None = Field(default=None, max_length=MAX_TARGET_LENGTH)


class RejectionReason(StrEnum):
    UNKNOWN_ACTION = "unknown_action"
    MALFORMED = "malformed"
    MISSING_TARGET = "missing_target"
    NO_SUCH_EXIT = "no_such_exit"
    REQUIREMENT_NOT_MET = "requirement_not_met"
    ITEM_NOT_HERE = "item_not_here"
    INVENTORY_FULL = "inventory_full"
    NOT_AVAILABLE = "not_available"
    GAME_OVER = "game_over"


class Rejection(FrozenModel):
    reason: RejectionReason
    message: str


class GameEvent(FrozenModel):
    # `kind` y `detail` bastan para que el narrador cuente lo ocurrido sin ver el estado.
    kind: str
    detail: str = ""


class ActionResult(FrozenModel):
    ok: bool
    rejection: Rejection | None = None
    events: tuple[GameEvent, ...] = ()


def reject(reason: RejectionReason, message: str) -> ActionResult:
    return ActionResult(ok=False, rejection=Rejection(reason=reason, message=message))


def parse_proposed_action(data: object) -> ProposedAction | Rejection:
    """Convierte datos no confiables en acción o en rechazo; nunca lanza (P7)."""
    if isinstance(data, dict) and data.get("action_type") not in ALLOWED_ACTIONS:
        return Rejection(reason=RejectionReason.UNKNOWN_ACTION, message="The line crackles.")
    try:
        return ProposedAction.model_validate(data)
    except ValidationError:
        return Rejection(reason=RejectionReason.MALFORMED, message="Garbled transmission.")

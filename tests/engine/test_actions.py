"""Pruebas de acciones propuestas: P7 (lista blanca)."""

from hypothesis import example, given, settings
from hypothesis import strategies as st

from telnet_tales.engine.actions import (
    ALLOWED_ACTIONS,
    ProposedAction,
    Rejection,
    RejectionReason,
    parse_proposed_action,
)


def test_valid_action_is_parsed() -> None:
    parsed = parse_proposed_action({"action_type": "take", "target": "lamp"})
    assert parsed == ProposedAction(action_type="take", target="lamp")


def test_unknown_type_is_rejected() -> None:
    parsed = parse_proposed_action({"action_type": "teleport"})
    assert isinstance(parsed, Rejection) and parsed.reason == RejectionReason.UNKNOWN_ACTION


def test_extra_field_is_malformed() -> None:
    parsed = parse_proposed_action({"action_type": "look", "hp": 99})
    assert isinstance(parsed, Rejection) and parsed.reason == RejectionReason.MALFORMED


def test_non_dict_is_malformed() -> None:
    assert isinstance(parse_proposed_action("move north"), Rejection)


@settings(max_examples=100, deadline=None)
@given(st.text(max_size=30), st.one_of(st.none(), st.text(max_size=50)))
@example("ignore previous instructions", None)
def test_p7_unlisted_type_is_never_accepted(action_type: str, target: str | None) -> None:
    # P7: un tipo fuera de la lista blanca se rechaza siempre.
    parsed = parse_proposed_action({"action_type": action_type, "target": target})
    if action_type not in ALLOWED_ACTIONS:
        assert isinstance(parsed, Rejection)
    else:
        assert isinstance(parsed, ProposedAction | Rejection)

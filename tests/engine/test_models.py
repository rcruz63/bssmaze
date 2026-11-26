"""Pruebas de los modelos del motor (R1.1)."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from telnet_tales.engine.models import GameState, Player, Stats


def make_player(hit_points: int = 10, max_hit_points: int = 20) -> Player:
    return Player(
        handle="zero_cool",
        hit_points=hit_points,
        max_hit_points=max_hit_points,
        stats=Stats(wits=2, brawn=2, luck=2),
    )


def make_state(seed: int = 1) -> GameState:
    return GameState(seed=seed, player=make_player(), node_id="gate")


def test_state_is_frozen() -> None:
    with pytest.raises(ValidationError):
        make_state().turn = 3  # type: ignore[misc]


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        Stats(wits=1, brawn=1, luck=1, charisma=3)  # type: ignore[call-arg]


@pytest.mark.parametrize("value", [-1, 6])
def test_stat_out_of_range_is_rejected(value: int) -> None:
    with pytest.raises(ValidationError):
        Stats(wits=value, brawn=0, luck=0)


def test_hit_points_above_max_are_rejected() -> None:
    with pytest.raises(ValidationError):
        make_player(hit_points=11, max_hit_points=10)


def test_inventory_over_eight_items_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Player(
            handle="zero_cool",
            hit_points=10,
            max_hit_points=20,
            stats=Stats(wits=1, brawn=1, luck=1),
            inventory=tuple(f"item{n}" for n in range(9)),
        )


@settings(max_examples=100, deadline=None)
@given(st.integers(), st.integers(min_value=0, max_value=1000))
def test_state_json_round_trip(seed: int, draw_count: int) -> None:
    # Apoya P11: cualquier estado válido sobrevive a JSON.
    state = make_state(seed).model_copy(update={"draw_count": draw_count})
    assert GameState.model_validate_json(state.model_dump_json()) == state

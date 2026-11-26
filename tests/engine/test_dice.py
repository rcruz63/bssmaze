"""Pruebas de dados con semilla: P1 (rango y regla) y P2 (determinismo)."""

from hypothesis import example, given, settings
from hypothesis import strategies as st

from telnet_tales.engine.dice import check, is_success, roll_d20
from telnet_tales.engine.models import GameState
from tests.engine.test_models import make_state

seeds = st.integers(min_value=-(2**63), max_value=2**63)


def test_roll_is_repeatable_and_counts_draws() -> None:
    first, state = roll_d20(make_state(42))
    assert roll_d20(make_state(42))[0] == first
    assert state.draw_count == 1


def test_natural_twenty_and_one_override_modifier() -> None:
    assert is_success(20, -100, 99)
    assert not is_success(1, 100, 2)


def test_ordinary_roll_follows_the_rule() -> None:
    assert is_success(10, 2, 12)
    assert not is_success(10, 1, 12)


def test_check_advances_draw_count_by_one() -> None:
    _, state = check(make_state(7), 0, 10)
    assert state.draw_count == 1


@settings(max_examples=100, deadline=None)
@given(seeds, st.integers(min_value=0, max_value=5), st.integers(min_value=1, max_value=30))
@example(0, 0, 1)
def test_p1_roll_in_range_and_outcome_matches_rule(seed: int, modifier: int, dc: int) -> None:
    # P1: tirada en 1..20 y resultado igual a la regla.
    result, _ = check(make_state(seed), modifier, dc)
    assert 1 <= result.roll <= 20
    assert result.total == result.roll + modifier
    expected = result.roll == 20 or (result.roll != 1 and result.total >= dc)
    assert result.success == expected


def roll_many(state: GameState, count: int) -> tuple[list[int], GameState]:
    rolls: list[int] = []
    for _ in range(count):
        roll, state = roll_d20(state)
        rolls.append(roll)
    return rolls, state


@settings(max_examples=100, deadline=None)
@given(seeds, st.integers(min_value=0, max_value=40))
def test_p2_same_seed_same_rolls_same_final_state(seed: int, count: int) -> None:
    # P2: misma semilla y mismas acciones dan el mismo estado final.
    assert roll_many(make_state(seed), count) == roll_many(make_state(seed), count)


@settings(max_examples=100, deadline=None)
@given(seeds, st.integers(min_value=0, max_value=30), st.integers(min_value=0, max_value=30))
def test_p2_resume_from_saved_state_continues_the_sequence(
    seed: int, before: int, after: int
) -> None:
    # P2 (reanudación): guardar y recargar a mitad no cambia las tiradas siguientes.
    whole, _ = roll_many(make_state(seed), before + after)
    _, mid = roll_many(make_state(seed), before)
    reloaded = GameState.model_validate_json(mid.model_dump_json())
    rest, _ = roll_many(reloaded, after)
    assert whole[before:] == rest

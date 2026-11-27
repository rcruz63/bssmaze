"""Pruebas de reglas: P3 (rechazo puro), P4 (vida), P5 (inventario), P2 (determinismo)."""

from hypothesis import given, settings
from hypothesis import strategies as st

from telnet_tales.engine.actions import ActionType, ProposedAction, RejectionReason
from telnet_tales.engine.models import MAX_INVENTORY, GameState
from telnet_tales.engine.rules import apply_action
from tests.engine.story_fixture import make_game, make_story

STORY = make_story()
TYPES: list[ActionType] = [
    "move", "look", "take", "use", "attack", "flee", "inventory", "help", "quit",
]  # fmt: skip
TARGETS = st.sampled_from([None, "", "north", "vault", "climb", "south", "iron key", "lamp", "x"])
actions = st.builds(ProposedAction, action_type=st.sampled_from(TYPES), target=TARGETS)


def run(state: GameState, script: list[ProposedAction]) -> GameState:
    for action in script:
        state, _ = apply_action(state, action, STORY)
    return state


def act(kind: ActionType, target: str | None = None) -> ProposedAction:
    return ProposedAction(action_type=kind, target=target)


def test_move_changes_node_and_counts_turn() -> None:
    state, result = apply_action(make_game(), act("move", "North"), STORY)
    assert result.ok and state.node_id == "hall" and state.turn == 1


def test_locked_exit_needs_item() -> None:
    state, result = apply_action(make_game(), act("move", "vault"), STORY)
    assert result.rejection and result.rejection.reason == RejectionReason.REQUIREMENT_NOT_MET
    assert state == make_game()


def test_item_requirement_opens_exit() -> None:
    state, _ = apply_action(make_game(), act("take", "iron key"), STORY)
    state, result = apply_action(state, act("move", "vault"), STORY)
    assert result.ok and state.node_id == "vault"


def test_stat_requirement() -> None:
    _, weak = apply_action(make_game(brawn=2), act("move", "climb"), STORY)
    _, strong = apply_action(make_game(brawn=3), act("move", "climb"), STORY)
    assert not weak.ok and strong.ok


def test_taken_item_is_gone_from_node() -> None:
    state, _ = apply_action(make_game(), act("take", "lamp"), STORY)
    _, again = apply_action(state, act("take", "lamp"), STORY)
    assert again.rejection and again.rejection.reason == RejectionReason.ITEM_NOT_HERE
    assert state.player.inventory == ("lamp",)


def test_full_pack_rejects_take() -> None:
    full = make_game(inventory=tuple(f"i{n}" for n in range(MAX_INVENTORY)))
    _, result = apply_action(full, act("take", "lamp"), STORY)
    assert result.rejection and result.rejection.reason == RejectionReason.INVENTORY_FULL


def test_missing_target_and_unavailable_and_game_over() -> None:
    assert apply_action(make_game(), act("move"), STORY)[1].rejection
    assert apply_action(make_game(), act("attack"), STORY)[1].rejection
    ended = make_game().model_copy(update={"node_id": "vault"})
    assert apply_action(ended, act("look"), STORY)[1].rejection


def test_look_and_inventory_do_not_change_state() -> None:
    for kind in ("look", "inventory", "help", "quit"):
        state, result = apply_action(make_game(), act(kind), STORY)
        assert result.ok and state == make_game()


@settings(max_examples=100, deadline=None)
@given(st.lists(actions, max_size=25))
def test_p3_rejected_action_leaves_state_equal(script: list[ProposedAction]) -> None:
    # P3: si el resultado no es ok, el estado devuelto es igual al de entrada.
    state = make_game()
    for action in script:
        new_state, result = apply_action(state, action, STORY)
        if not result.ok:
            assert new_state == state
        state = new_state


@settings(max_examples=100, deadline=None)
@given(st.lists(actions, max_size=40))
def test_p4_p5_bounds_hold_after_any_sequence(script: list[ProposedAction]) -> None:
    # P4: la vida queda en 0..max. P5: mochila <= 8 y sin duplicados.
    final = run(make_game(), script)
    assert 0 <= final.player.hit_points <= final.player.max_hit_points
    assert len(final.player.inventory) <= MAX_INVENTORY
    assert len(set(final.player.inventory)) == len(final.player.inventory)


@settings(max_examples=100, deadline=None)
@given(st.lists(actions, max_size=30))
def test_p2_same_script_same_final_state(script: list[ProposedAction]) -> None:
    # P2: mismas acciones y misma semilla dan el mismo estado final.
    assert run(make_game(), script) == run(make_game(), script)

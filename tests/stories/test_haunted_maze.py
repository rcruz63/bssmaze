"""El borrador de "The Haunted Maze" es válido, ganable y respeta el ancho (R2.4)."""

from itertools import chain
from pathlib import Path

from telnet_tales.engine.actions import ProposedAction
from telnet_tales.engine.rules import apply_action
from telnet_tales.engine.story_models import Story
from telnet_tales.stories.graph import is_winnable
from telnet_tales.stories.loader import load_story
from tests.engine.test_models import make_state

PATH = Path(__file__).parent.parent.parent / "stories" / "haunted_maze.yaml"
WINNING_SCRIPT = [
    ("move", "north"), ("take", "lantern"), ("move", "down"), ("move", "east"),
    ("take", "iron_key"), ("move", "north"), ("move", "north"), ("move", "exit"),
]  # fmt: skip


def story() -> Story:
    return load_story(PATH)


def test_shape_matches_the_spec() -> None:
    loaded = story()
    assert 12 <= len(loaded.nodes) <= 15
    assert len(loaded.encounters) == 2
    assert {n.outcome for n in loaded.nodes.values() if n.is_ending} == {"victory", "defeat"}


def test_story_is_a_marked_draft() -> None:
    lines = PATH.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# draft: tone and difficulty need human review"
    assert "status: draft" in lines


def test_story_is_winnable_through_the_key() -> None:
    assert is_winnable(story())
    items = list(chain.from_iterable(n.items for n in story().nodes.values()))
    assert items.count("iron_key") == 1


def test_art_lines_fit_78_columns() -> None:
    texts = [n.text for n in story().nodes.values()]
    lines = list(chain.from_iterable(map(str.splitlines, texts)))
    assert max(map(len, lines)) <= 78


def test_engine_can_walk_the_winning_path() -> None:
    loaded = story()
    state = make_state().model_copy(update={"node_id": loaded.start})
    for kind, target in WINNING_SCRIPT:
        action = ProposedAction(action_type=kind, target=target)
        state, result = apply_action(state, action, loaded)
        assert result.ok, (kind, target)
    assert loaded.nodes[state.node_id].outcome == "victory"

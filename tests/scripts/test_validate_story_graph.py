from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from story_validation.checks import display_width, validate_story
from validate_story_graph import main

FIXTURE = Path(__file__).parent.parent / "fixtures" / "valid_story.yaml"


def story(*nodes: dict[str, object], start: str = "a") -> dict[str, object]:
    return {"start": start, "nodes": list(nodes)}


def ending(name: str) -> dict[str, object]:
    return {"id": name, "exits": [], "is_ending": True}


def linked(name: str, target: str) -> dict[str, object]:
    return {"id": name, "exits": [{"label": "go", "target_id": target}]}


def errors(data: object) -> list[str]:
    return [i.message for i in validate_story(data) if i.severity == "error"]


def test_fixture_is_valid() -> None:
    assert main(["x", str(FIXTURE.parent)]) == 0


def test_missing_target_is_an_error() -> None:
    assert "does not exist" in errors(story(linked("a", "zzz"), ending("b")))[0]


def test_dead_end_without_is_ending_is_an_error() -> None:
    assert "is_ending" in errors(story(linked("a", "b"), {"id": "b", "exits": []}))[0]


def test_line_over_80_columns_is_an_error() -> None:
    node = {"id": "a", "text": "x" * 81, "exits": [], "is_ending": True}
    assert "81 columns" in errors(story(node))[0]


def test_wide_characters_count_double() -> None:
    assert display_width("日本") == 4


def test_unreachable_node_is_only_a_warning() -> None:
    issues = validate_story(story(ending("a"), ending("lost")))
    assert [i.severity for i in issues] == ["warning"]


def test_unreadable_story_fails(tmp_path: Path) -> None:
    (tmp_path / "bad.yaml").write_text("a: [", encoding="utf-8")
    assert main(["x", str(tmp_path)]) == 1


def chain(size: int, extra: list[tuple[int, int]]) -> list[dict[str, object]]:
    """Cadena 0->1->...->fin, más aristas extra entre nodos existentes."""
    names = [f"n{i}" for i in range(size)]
    nodes = [linked(names[i], names[i + 1]) for i in range(size - 1)]
    for source, target in extra:
        exits = nodes[source % (size - 1)]["exits"]
        assert isinstance(exits, list)
        exits.append({"label": "x", "target_id": names[target % size]})
    return [*nodes, ending(names[-1])]


edges = st.lists(st.tuples(st.integers(0, 50), st.integers(0, 50)), max_size=8)


@settings(max_examples=100, deadline=None)
@given(size=st.integers(2, 12), extra=edges)
def test_generated_valid_graphs_pass(size: int, extra: list[tuple[int, int]]) -> None:
    assert validate_story(story(*chain(size, extra), start="n0")) == []


@settings(max_examples=100, deadline=None)
@given(size=st.integers(2, 12), extra=edges, victim=st.integers(0, 50))
def test_broken_edge_is_always_caught(size: int, extra: list[tuple[int, int]], victim: int) -> None:
    nodes = chain(size, extra)
    exits = nodes[victim % (size - 1)]["exits"]
    assert isinstance(exits, list)
    exits[0]["target_id"] = "missing_node"
    assert any("missing_node" in message for message in errors(story(*nodes, start="n0")))

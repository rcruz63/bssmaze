"""Pruebas del validador de grafo: P6."""

from hypothesis import example, given, settings
from hypothesis import strategies as st

from telnet_tales.engine.story_models import Exit, Requirement, Story, StoryNode
from telnet_tales.stories.graph import closure, is_winnable, validate_graph
from tests.engine.story_fixture import make_story


def build(spec: dict[str, tuple[list[str], bool]], start: str = "n0") -> Story:
    nodes = {
        name: StoryNode(
            id=name,
            title=name,
            text="t",
            exits=tuple(Exit(label=f"to_{t}", target_id=t) for t in targets),
            is_ending=ending,
        )
        for name, (targets, ending) in spec.items()
    }
    return Story(start=start, nodes=nodes)


def test_fixture_story_is_valid() -> None:
    assert validate_graph(make_story()) == []


def test_unknown_target_unreachable_and_dead_end_are_found() -> None:
    story = build({"n0": (["zz"], False), "n1": ([], False)})
    text = "\n".join(validate_graph(story))
    assert "zz" in text and "unreachable" in text and "no exits" in text
    assert "no is_ending" in text


def test_node_that_cannot_finish_is_found() -> None:
    story = build({"n0": (["n1", "n2"], False), "n1": (["n1"], False), "n2": ([], True)})
    assert any("cannot reach any ending" in e for e in validate_graph(story))


def test_missing_start_and_empty_story() -> None:
    assert validate_graph(build({"n0": ([], True)}, start="x"))
    assert validate_graph(Story(start="a", nodes={})) == ["story has no nodes"]


def test_required_item_that_exists_nowhere_is_found() -> None:
    node = StoryNode(
        id="a",
        title="a",
        text="t",
        exits=(Exit(label="x", target_id="b", requirement=Requirement(item="ghost")),),
    )
    end = StoryNode(id="b", title="b", text="t", is_ending=True)
    story = Story(start="a", nodes={"a": node, "b": end})
    assert any("ghost" in e for e in validate_graph(story))


def test_unknown_encounter_is_found() -> None:
    node = StoryNode(id="a", title="a", text="t", encounter="boo", is_ending=True)
    assert any("boo" in e for e in validate_graph(Story(start="a", nodes={"a": node})))


def test_winnable_needs_victory_outcome_and_items() -> None:
    assert not is_winnable(make_story())  # el final del fixture no declara victoria
    vault = StoryNode(id="vault", title="v", text="t", is_ending=True, outcome="victory")
    nodes = {**make_story().nodes, "vault": vault}
    assert is_winnable(Story(start="gate", nodes=nodes))
    no_key = {**nodes, "gate": nodes["gate"].model_copy(update={"items": ("lamp",)})}
    assert not is_winnable(Story(start="gate", nodes=no_key))


names = st.sampled_from([f"n{i}" for i in range(5)])
specs = st.dictionaries(names, st.tuples(st.lists(names, max_size=3), st.booleans()), min_size=1)


def reaches(source: str, goal: set[str], spec: dict[str, tuple[list[str], bool]]) -> bool:
    return source in goal or bool(
        closure([source], {k: tuple(v[0]) for k, v in spec.items()}) & goal
    )


@settings(max_examples=100, deadline=None)
@given(specs)
@example({"n0": (["n0"], True)})
def test_p6_valid_story_reaches_everything_and_ends(
    spec: dict[str, tuple[list[str], bool]],
) -> None:
    # P6: si no hay errores, todo nodo es alcanzable desde el inicio y llega a un final.
    start = next(iter(spec))
    if validate_graph(build(spec, start)):
        return
    endings = {name for name, (_, ending) in spec.items() if ending}
    edges = {k: tuple(v[0]) for k, v in spec.items()}
    assert closure([start], edges) == set(spec)
    assert all(reaches(name, endings, spec) for name in spec)

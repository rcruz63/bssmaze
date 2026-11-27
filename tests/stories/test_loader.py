"""Pruebas del cargador: errores agregados (R2.3)."""

from pathlib import Path

import pytest

from telnet_tales.stories.loader import StoryLoadError, load_story, parse_story

FIXTURE = Path(__file__).parent.parent / "fixtures" / "valid_story.yaml"


def node(name: str, target: str | None = None, ending: bool = False) -> dict[str, object]:
    exits = [{"label": "go", "target_id": target}] if target else []
    return {"id": name, "title": name, "text": "t", "exits": exits, "is_ending": ending}


def test_valid_fixture_loads() -> None:
    assert load_story(FIXTURE).start == "gate"


def test_all_errors_are_listed_together() -> None:
    data = {"start": "zzz", "nodes": [node("a", "nowhere"), node("b")]}
    with pytest.raises(StoryLoadError) as caught:
        parse_story(data)
    text = "\n".join(caught.value.errors)
    assert "zzz" in text and "nowhere" in text and "no exits" in text


def test_schema_errors_are_reported() -> None:
    with pytest.raises(StoryLoadError) as caught:
        parse_story({"start": "a", "nodes": [{"id": "a"}]})
    assert any("title" in error for error in caught.value.errors)


def test_duplicate_ids_are_reported() -> None:
    data = {"start": "a", "nodes": [node("a", "a"), node("a", ending=True)]}
    with pytest.raises(StoryLoadError, match="duplicate"):
        parse_story(data)


def test_missing_file_is_a_load_error(tmp_path: Path) -> None:
    with pytest.raises(StoryLoadError, match="cannot read"):
        load_story(tmp_path / "nope.yaml")


def test_broken_yaml_is_a_load_error(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("start: [unclosed", encoding="utf-8")
    with pytest.raises(StoryLoadError):
        load_story(path)

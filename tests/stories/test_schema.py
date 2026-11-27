"""Pruebas del esquema de historia."""

import pytest
from pydantic import ValidationError

from telnet_tales.stories.schema import Requirement, StoryFile


def test_requirement_needs_exactly_one_condition() -> None:
    with pytest.raises(ValidationError):
        Requirement()
    with pytest.raises(ValidationError):
        Requirement(item="key", stat="wits")


def test_unknown_field_is_rejected() -> None:
    data = {"start": "a", "nodes": [{"id": "a", "title": "A", "text": "t", "mood": "x"}]}
    with pytest.raises(ValidationError):
        StoryFile.model_validate(data)


def test_to_story_indexes_nodes_and_encounters() -> None:
    data = {
        "start": "a",
        "nodes": [{"id": "a", "title": "A", "text": "t", "is_ending": True}],
        "encounters": [{"id": "e", "name": "E", "hit_points": 3, "attack_bonus": 1, "damage": 2}],
    }
    story = StoryFile.model_validate(data).to_story()
    assert list(story.nodes) == ["a"] and "e" in story.encounters

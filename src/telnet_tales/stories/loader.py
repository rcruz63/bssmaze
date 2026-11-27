"""Carga de historias desde YAML con errores agregados (R2.1, R2.3)."""

from collections import Counter
from pathlib import Path

import yaml
from pydantic import ValidationError

from telnet_tales.engine.story_models import Story
from telnet_tales.stories.graph import validate_graph
from telnet_tales.stories.schema import StoryFile


class StoryLoadError(Exception):
    """Lleva todos los errores a la vez: el autor corrige la historia de una sola pasada."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def _read_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise StoryLoadError([f"cannot read story: {error}"]) from error


def _location(path: tuple[int | str, ...]) -> str:
    return ".".join(map(str, path))


def _schema_errors(error: ValidationError) -> list[str]:
    return [f"{_location(e['loc'])}: {e['msg']}" for e in error.errors()]


def _parse_file(data: object) -> StoryFile:
    try:
        return StoryFile.model_validate(data)
    except ValidationError as error:
        raise StoryLoadError(_schema_errors(error)) from error


def _duplicate_ids(story_file: StoryFile) -> list[str]:
    counts = Counter(node.id for node in story_file.nodes)
    return [f"duplicate node id {name!r}" for name, total in counts.items() if total > 1]


def parse_story(data: object) -> Story:
    """Valida esquema y grafo; si algo falla, lanza un único error con la lista completa."""
    story_file = _parse_file(data)
    errors = _duplicate_ids(story_file)
    if errors:
        raise StoryLoadError(errors)
    story = story_file.to_story()
    errors = validate_graph(story)
    if errors:
        raise StoryLoadError(errors)
    return story


def load_story(path: Path) -> Story:
    return parse_story(_read_yaml(path))

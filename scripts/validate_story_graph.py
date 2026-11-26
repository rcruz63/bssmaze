"""Valida los archivos de `stories/`: destinos, callejones sin salida y anchura de 80 columnas."""

import json
import sys
from itertools import chain
from pathlib import Path

import yaml

from story_validation.checks import validate_story
from story_validation.issues import Issue

STORY_SUFFIXES = {".yaml", ".yml", ".json"}


def find_story_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in STORY_SUFFIXES)


def load_file(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)


def validate_file(path: Path) -> list[Issue]:
    """Un archivo ilegible es un hallazgo más, no una excepción que oculte los demás."""
    try:
        return validate_story(load_file(path))
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [Issue("error", f"cannot read story: {error}")]


def report_file(path: Path) -> list[tuple[Path, Issue]]:
    return [(path, issue) for issue in validate_file(path)]


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("stories")
    reports = list(chain.from_iterable(map(report_file, find_story_files(root))))
    for path, issue in reports:
        print(issue.render(str(path)))
    return 1 if any(issue.severity == "error" for _, issue in reports) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""Verifica que ningún archivo del repositorio supere el límite duro de líneas."""

import sys
from pathlib import Path

HARD_LIMIT = 200  # Límite duro: un archivo más largo ya mezcla responsabilidades.
SOFT_LIMIT = 150  # Objetivo: avisar antes de llegar al límite duro.
CHECKED_SUFFIXES = {".py", ".md", ".json", ".yaml", ".yml", ".toml", ".sh"}
IGNORED_DIRS = {".git", ".venv", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
IGNORED_FILES = {"uv.lock"}  # Archivo generado: no se puede dividir.
HYPOTHESIS_DIR = ".hypothesis"


def is_checked(path: Path, root: Path) -> bool:
    """Decide si un archivo cuenta para el límite (ignora generados y cachés)."""
    parts = set(path.relative_to(root).parts)
    if parts & IGNORED_DIRS or HYPOTHESIS_DIR in parts:
        return False
    return path.suffix in CHECKED_SUFFIXES and path.name not in IGNORED_FILES


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def find_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and is_checked(p, root))


def find_violations(root: Path, limit: int = HARD_LIMIT) -> dict[Path, int]:
    """Devuelve los archivos que superan `limit`, con su número de líneas."""
    counts = {path: count_lines(path) for path in find_files(root)}
    return {path: total for path, total in counts.items() if total > limit}


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    violations = find_violations(root)
    for path, total in violations.items():
        print(f"{path.relative_to(root)}: {total} líneas (máximo {HARD_LIMIT})")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

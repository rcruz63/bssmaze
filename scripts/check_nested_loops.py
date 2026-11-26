"""Detecta bucles anidados (regla del proyecto: CERO bucles anidados).

Marca `for`/`while` dentro de otro bucle y comprensiones con varias cláusulas
`for`, o comprensiones dentro de un bucle, dentro de una misma función.
"""

import ast
import sys
from itertools import chain
from pathlib import Path

LOOPS = (ast.For, ast.While, ast.AsyncFor)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
IGNORED_DIRS = {".git", ".venv", "__pycache__", ".mypy_cache", ".ruff_cache"}


class LoopNestingFinder(ast.NodeVisitor):
    """Recorre un árbol llevando la profundidad de iteración de la función actual."""

    def __init__(self) -> None:
        self.depth = 0
        self.lines: list[int] = []

    def _enter_iteration(self, node: ast.AST, extra_levels: int = 1) -> None:
        if self.depth > 0 or extra_levels > 1:
            self.lines.append(getattr(node, "lineno", 0))
        self.depth += extra_levels
        self.generic_visit(node)
        self.depth -= extra_levels

    def visit_For(self, node: ast.For) -> None:
        self._enter_iteration(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._enter_iteration(node)

    def visit_While(self, node: ast.While) -> None:
        self._enter_iteration(node)

    def _visit_comprehension(self, node: ast.AST) -> None:
        generators = getattr(node, "generators", [])
        self._enter_iteration(node, extra_levels=len(generators))

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node)

    def _visit_function(self, node: ast.AST) -> None:
        # Una función anidada es otra unidad: su profundidad empieza de cero.
        saved_depth, self.depth = self.depth, 0
        self.generic_visit(node)
        self.depth = saved_depth

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self._visit_function(node)


def find_nested_loop_lines(source: str) -> list[int]:
    finder = LoopNestingFinder()
    finder.visit(ast.parse(source))
    return sorted(set(finder.lines))


def python_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.py") if not set(p.parts) & IGNORED_DIRS)


def report_file(path: Path) -> int:
    """Imprime los bucles anidados de un archivo y devuelve cuántos hay."""
    lines = find_nested_loop_lines(path.read_text(encoding="utf-8"))
    for line in lines:
        print(f"{path}:{line}: bucle anidado")
    return len(lines)


def main(argv: list[str]) -> int:
    roots = [Path(arg) for arg in argv[1:]] or [Path("src"), Path("scripts")]
    files = list(chain.from_iterable(map(python_files, roots)))
    return 1 if sum(report_file(path) for path in files) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

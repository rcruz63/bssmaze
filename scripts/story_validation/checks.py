"""Comprobaciones puras sobre los nodos de una historia."""

import unicodedata
from itertools import chain

from story_validation.issues import Issue
from story_validation.nodes import Node, exits_of, iter_strings, node_id, split_story, target_ids

MAX_COLUMNS = 80  # Mismo límite que el renderizador: una línea más larga se partiría en pantalla.


def display_width(line: str) -> int:
    """Cuenta columnas de pantalla, no bytes: los caracteres anchos ocupan dos."""
    wide = sum(unicodedata.east_asian_width(char) in "WF" for char in line)
    combining = sum(unicodedata.combining(char) > 0 for char in line)
    return len(line) + wide - combining


def check_start(start: str | None, ids: set[str]) -> list[Issue]:
    if start is None or start not in ids:
        return [Issue("error", f"start node {start!r} does not exist")]
    return []


def check_duplicate_ids(nodes: list[Node]) -> list[Issue]:
    ids = [node_id(node) for node in nodes]
    return [
        Issue("error", f"duplicate node id {name!r}")
        for name in sorted(set(ids))
        if ids.count(name) > 1
    ]


def node_targets(node: Node) -> list[tuple[str, str]]:
    return [(node_id(node), target) for target in target_ids(node)]


def node_lines(node: Node) -> list[tuple[str, str]]:
    texts = chain.from_iterable(text.splitlines() for text in iter_strings(node))
    return [(node_id(node), line) for line in texts]


def check_targets(nodes: list[Node], ids: set[str]) -> list[Issue]:
    pairs = list(chain.from_iterable(map(node_targets, nodes)))
    return [
        Issue("error", f"node {source!r}: exit target_id {target!r} does not exist")
        for source, target in pairs
        if target not in ids
    ]


def check_dead_ends(nodes: list[Node]) -> list[Issue]:
    return [
        Issue("error", f"node {node_id(node)!r} has no exits and is not is_ending: true")
        for node in nodes
        if not exits_of(node) and node.get("is_ending") is not True
    ]


def check_line_widths(nodes: list[Node]) -> list[Issue]:
    lines = list(chain.from_iterable(map(node_lines, nodes)))
    return [
        Issue("error", f"node {name!r}: line is {display_width(line)} columns (max {MAX_COLUMNS})")
        for name, line in lines
        if display_width(line) > MAX_COLUMNS
    ]


def reachable_from(start: str, nodes: list[Node]) -> set[str]:
    """Búsqueda en anchura con una pila; los destinos inexistentes se ignoran aquí."""
    edges = {node_id(node): target_ids(node) for node in nodes}
    seen: set[str] = set()
    pending = [start]
    while pending:
        current = pending.pop()
        if current not in seen and current in edges:
            seen.add(current)
            pending.extend(edges[current])
    return seen


def check_reachability(start: str | None, nodes: list[Node]) -> list[Issue]:
    if start is None:
        return []
    seen = reachable_from(start, nodes)
    return [
        Issue("warning", f"node {node_id(node)!r} is unreachable from start {start!r}")
        for node in nodes
        if node_id(node) not in seen
    ]


def validate_story(data: object) -> list[Issue]:
    """Ejecuta todas las comprobaciones; nunca lanza por datos mal formados."""
    start, nodes = split_story(data)
    if not nodes:
        return [Issue("error", "story has no nodes")]
    ids = {node_id(node) for node in nodes}
    return [
        *check_start(start, ids),
        *check_duplicate_ids(nodes),
        *check_targets(nodes, ids),
        *check_dead_ends(nodes),
        *check_line_widths(nodes),
        *check_reachability(start, nodes),
    ]

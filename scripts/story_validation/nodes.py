"""Lectura tolerante de nodos: los datos vienen de un archivo editado a mano."""

from collections.abc import Iterator
from itertools import chain

# Los archivos YAML/JSON son una frontera de confianza: el contenido es desconocido.
Node = dict[str, object]


def split_story(data: object) -> tuple[str | None, list[Node]]:
    """Acepta una lista de nodos o un mapa `{start, nodes}`; el inicio por defecto es el primero."""
    if isinstance(data, dict):
        raw_nodes, start = data.get("nodes"), data.get("start")
    else:
        raw_nodes, start = data, None
    nodes = (
        [item for item in raw_nodes if isinstance(item, dict)]
        if isinstance(raw_nodes, list)
        else []
    )
    if not isinstance(start, str) and nodes:
        start = str(nodes[0].get("id"))
    return (start if isinstance(start, str) else None), nodes


def node_id(node: Node) -> str:
    return str(node.get("id", "?"))


def exits_of(node: Node) -> list[Node]:
    raw = node.get("exits")
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def target_ids(node: Node) -> list[str]:
    """Los `target_id` declarados; un valor ausente se informa como cadena vacía."""
    return [str(exit_.get("target_id", "")) for exit_ in exits_of(node)]


def iter_strings(value: object) -> Iterator[str]:
    """Recorre todas las cadenas: el arte ASCII puede estar en cualquier campo."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        yield from iter_strings(list(value.values()))
    elif isinstance(value, list):
        yield from chain.from_iterable(map(iter_strings, value))

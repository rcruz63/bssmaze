"""Validador de grafo en tiempo de ejecución (R2.2). Mismo vocabulario que el script."""

from collections.abc import Mapping
from itertools import chain

from telnet_tales.engine.story_models import Exit, Story, StoryNode

Edges = Mapping[str, tuple[str, ...]]


def targets_of(node: StoryNode, held: frozenset[str] | None = None) -> tuple[str, ...]:
    """Destinos de un nodo; con `held`, solo las salidas cuyo objeto requerido se tiene."""
    return tuple(e.target_id for e in node.exits if held is None or exit_is_open(e, held))


def exit_is_open(exit_: Exit, held: frozenset[str]) -> bool:
    # Los requisitos de característica se suponen cumplidos: dependen del personaje.
    requirement = exit_.requirement
    return requirement is None or requirement.item is None or requirement.item in held


def node_exit_pairs(node: StoryNode) -> list[tuple[StoryNode, Exit]]:
    return [(node, e) for e in node.exits]


def exit_pairs(story: Story) -> list[tuple[StoryNode, Exit]]:
    return list(chain.from_iterable(map(node_exit_pairs, story.nodes.values())))


def forward_edges(story: Story) -> dict[str, tuple[str, ...]]:
    return {n.id: targets_of(n) for n in story.nodes.values()}


def closure(starts: list[str], edges: Edges) -> set[str]:
    """Nodos alcanzables con una pila; los ids desconocidos se ignoran (se informan aparte)."""
    seen: set[str] = set()
    pending = list(starts)
    while pending:
        current = pending.pop()
        if current not in seen and current in edges:
            seen.add(current)
            pending.extend(edges[current])
    return seen


def edge_pairs(item: tuple[str, tuple[str, ...]]) -> list[tuple[str, str]]:
    source, targets = item
    return [(target, source) for target in targets]


def reverse_edges(edges: Edges) -> dict[str, tuple[str, ...]]:
    """Aristas invertidas, indexadas por destino, para preguntar quién llega a un final."""
    reverse: dict[str, list[str]] = {node: [] for node in edges}
    for target, source in chain.from_iterable(map(edge_pairs, edges.items())):
        reverse.setdefault(target, []).append(source)
    return {node: tuple(sources) for node, sources in reverse.items()}


def check_start(story: Story) -> list[str]:
    return [] if story.start in story.nodes else [f"start node {story.start!r} does not exist"]


def check_targets(story: Story) -> list[str]:
    return [
        f"node {n.id!r}: exit target_id {e.target_id!r} does not exist"
        for n, e in exit_pairs(story)
        if e.target_id not in story.nodes
    ]


def check_encounters(story: Story) -> list[str]:
    return [
        f"node {n.id!r}: unknown encounter {n.encounter!r}"
        for n in story.nodes.values()
        if n.encounter is not None and n.encounter not in story.encounters
    ]


def all_items(story: Story) -> set[str]:
    return set(chain.from_iterable(node.items for node in story.nodes.values()))


def check_required_items(story: Story) -> list[str]:
    known = all_items(story)
    return [
        f"node {n.id!r}: exit {e.label!r} needs item {e.requirement.item!r} that exists nowhere"
        for n, e in exit_pairs(story)
        if e.requirement and e.requirement.item and e.requirement.item not in known
    ]


def check_dead_ends(story: Story) -> list[str]:
    return [
        f"node {n.id!r} has no exits and is not is_ending: true"
        for n in story.nodes.values()
        if not n.exits and not n.is_ending
    ]


def endings(story: Story) -> list[StoryNode]:
    return [n for n in story.nodes.values() if n.is_ending]


def check_reachability(story: Story) -> list[str]:
    edges = forward_edges(story)
    seen = closure([story.start], edges)
    can_finish = closure([n.id for n in endings(story)], reverse_edges(edges))
    unreachable = [f"node {i!r} is unreachable from start" for i in edges if i not in seen]
    stuck = [f"node {i!r} cannot reach any ending" for i in edges if i not in can_finish]
    return [*unreachable, *stuck]


def validate_graph(story: Story) -> list[str]:
    """Devuelve todos los errores; una lista vacía cumple la propiedad P6."""
    if not story.nodes:
        return ["story has no nodes"]
    checks = (
        check_start,
        check_targets,
        check_encounters,
        check_required_items,
        check_dead_ends,
        check_reachability,
    )
    errors = list(chain.from_iterable(check(story) for check in checks))
    return errors if endings(story) else [*errors, "story has no is_ending node"]


def items_in(story: Story, node_ids: set[str]) -> set[str]:
    return set(chain.from_iterable(story.nodes[i].items for i in node_ids))


def reachable_with_items(story: Story, held: frozenset[str] = frozenset()) -> set[str]:
    """Punto fijo: recoger objetos abre salidas que dan acceso a más objetos."""
    edges = {n.id: targets_of(n, held) for n in story.nodes.values()}
    nodes = closure([story.start], edges)
    gained = held | items_in(story, nodes)
    return nodes if gained == held else reachable_with_items(story, frozenset(gained))


def is_winnable(story: Story) -> bool:
    """Hay un final de victoria alcanzable recogiendo objetos por el camino."""
    reachable = reachable_with_items(story)
    return any(story.nodes[i].outcome == "victory" for i in reachable if story.nodes[i].is_ending)

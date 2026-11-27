"""Historia mínima compartida por las pruebas del motor."""

from telnet_tales.engine.models import GameState, Player, Stats
from telnet_tales.engine.story_models import Exit, Requirement, Story, StoryNode


def make_story() -> Story:
    nodes = [
        StoryNode(
            id="gate",
            title="Gate",
            text="A gate.",
            exits=(
                Exit(label="north", target_id="hall"),
                Exit(label="vault", target_id="vault", requirement=Requirement(item="iron_key")),
                Exit(
                    label="climb",
                    target_id="hall",
                    requirement=Requirement(stat="brawn", minimum=3),
                ),
            ),
            items=("iron_key", "lamp"),
        ),
        StoryNode(
            id="hall", title="Hall", text="A hall.", exits=(Exit(label="south", target_id="gate"),)
        ),
        StoryNode(id="vault", title="Vault", text="Free.", is_ending=True),
    ]
    return Story(start="gate", nodes={node.id: node for node in nodes})


def make_game(brawn: int = 1, inventory: tuple[str, ...] = ()) -> GameState:
    stats = Stats(wits=1, brawn=brawn, luck=1)
    player = Player(
        handle="ana", hit_points=10, max_hit_points=20, stats=stats, inventory=inventory
    )
    return GameState(seed=1, player=player, node_id="gate")

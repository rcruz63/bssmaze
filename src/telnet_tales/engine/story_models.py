"""Datos de historia que el motor necesita para validar acciones (R2.1)."""

from typing import Literal, Self

from pydantic import Field, model_validator

from telnet_tales.engine.models import MAX_MODIFIER, FrozenModel

StatName = Literal["wits", "brawn", "luck"]


class Requirement(FrozenModel):
    # Los modelos viven en `engine` porque `rules` debe validar salidas sin importar `stories`
    # (la dependencia va de `stories` hacia `engine`, nunca al revés).
    item: str | None = None
    stat: StatName | None = None
    minimum: int = Field(default=1, ge=0, le=MAX_MODIFIER)

    @model_validator(mode="after")
    def _exactly_one_condition(self) -> Self:
        # Una condición doble sería ambigua para el jugador y para el narrador.
        if (self.item is None) == (self.stat is None):
            raise ValueError("requirement needs exactly one of item or stat")
        return self


class Exit(FrozenModel):
    label: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    requirement: Requirement | None = None


class Encounter(FrozenModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    hit_points: int = Field(ge=1)
    attack_bonus: int = Field(ge=0)
    damage: int = Field(ge=1)
    flavor_hint: str = ""


class StoryNode(FrozenModel):
    id: str = Field(min_length=1)
    title: str
    text: str
    exits: tuple[Exit, ...] = ()
    items: tuple[str, ...] = ()
    encounter: str | None = None
    is_ending: bool = False


class Story(FrozenModel):
    start: str
    nodes: dict[str, StoryNode]
    encounters: dict[str, Encounter] = {}

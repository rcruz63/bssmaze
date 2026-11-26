"""Modelos de estado del motor: inmutables, validados y sin E/S."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

MAX_HIT_POINTS = 20  # Tope de vida del diseño de juego.
MAX_MODIFIER = 5  # Los modificadores suman a un d20; más de 5 rompería el equilibrio.
MAX_INVENTORY = 8  # Mochila pequeña: obliga a elegir objetos.


class FrozenModel(BaseModel):
    # Inmutable y estricto: un estado que no cambia hace trivial comparar y repetir partidas.
    model_config = ConfigDict(frozen=True, extra="forbid")


class Stats(FrozenModel):
    wits: int = Field(ge=0, le=MAX_MODIFIER)
    brawn: int = Field(ge=0, le=MAX_MODIFIER)
    luck: int = Field(ge=0, le=MAX_MODIFIER)


class Player(FrozenModel):
    handle: str = Field(min_length=1, max_length=20)
    hit_points: int = Field(ge=0, le=MAX_HIT_POINTS)
    max_hit_points: int = Field(ge=1, le=MAX_HIT_POINTS)
    stats: Stats
    inventory: tuple[str, ...] = Field(default=(), max_length=MAX_INVENTORY)

    @model_validator(mode="after")
    def _hit_points_within_max(self) -> Self:
        # La vida actual nunca supera el máximo (propiedad P4 desde la construcción).
        if self.hit_points > self.max_hit_points:
            raise ValueError("hit_points cannot exceed max_hit_points")
        return self


class GameState(FrozenModel):
    # `seed` y `draw_count` bastan para reconstruir la RNG y repetir la partida (R1.3).
    # `combat` y `events` llegan con las tareas 10 y 2; no se adelantan aquí.
    seed: int
    draw_count: int = Field(default=0, ge=0)
    player: Player
    node_id: str = Field(min_length=1)
    flags: frozenset[str] = frozenset()
    turn: int = Field(default=0, ge=0)

"""Dados con semilla: funciones puras que devuelven el estado nuevo (R1.2, R1.3)."""

import random
from typing import NamedTuple

from telnet_tales.engine.models import GameState

D20_SIDES = 20


class CheckResult(NamedTuple):
    roll: int
    total: int
    success: bool


def _rng_at(seed: int, draw_count: int) -> random.Random:
    # shortcut: se reconstruye la RNG repitiendo `draw_count` tiradas (coste lineal);
    # cambiar a guardar el estado interno de Random si una partida pasa de miles de tiradas.
    rng = random.Random(seed)
    for _ in range(draw_count):
        rng.randint(1, D20_SIDES)
    return rng


def roll_d20(state: GameState) -> tuple[int, GameState]:
    """Tira un d20 con la RNG del estado y devuelve el estado con una tirada más."""
    rng = _rng_at(state.seed, state.draw_count)
    roll = rng.randint(1, D20_SIDES)
    return roll, state.model_copy(update={"draw_count": state.draw_count + 1})


def is_success(roll: int, modifier: int, difficulty_class: int) -> bool:
    # 20 natural siempre acierta y 1 natural siempre falla, sea cual sea el modificador.
    if roll == D20_SIDES:
        return True
    if roll == 1:
        return False
    return roll + modifier >= difficulty_class


def check(state: GameState, modifier: int, difficulty_class: int) -> tuple[CheckResult, GameState]:
    """Resuelve `d20 + modificador >= dificultad` y devuelve el estado avanzado."""
    roll, next_state = roll_d20(state)
    success = is_success(roll, modifier, difficulty_class)
    return CheckResult(roll, roll + modifier, success), next_state

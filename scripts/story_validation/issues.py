"""Tipo común de hallazgo para todas las comprobaciones de historias."""

from typing import Literal, NamedTuple


class Issue(NamedTuple):
    """Un problema encontrado; los `error` rompen el build, los `warning` solo avisan."""

    severity: Literal["error", "warning"]
    message: str

    def render(self, source: str) -> str:
        return f"{source}: {self.severity}: {self.message}"

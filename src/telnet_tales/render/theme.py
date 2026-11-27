"""Temas fósforo verde y ámbar: roles semánticos a colores ANSI de 16 (R6.2)."""

from enum import StrEnum
from typing import Literal

RESET = "\x1b[0m"


class Role(StrEnum):
    TITLE = "title"
    BODY = "body"
    DANGER = "danger"
    SYSTEM = "system"


ThemeName = Literal["green", "amber"]

# Solo SGR 1, 30-37 y 90-97 (steering retro-terminal): el código usa roles, nunca colores.
THEMES: dict[ThemeName, dict[Role, str]] = {
    "green": {Role.TITLE: "1;92", Role.BODY: "32", Role.DANGER: "1;91", Role.SYSTEM: "92"},
    "amber": {Role.TITLE: "1;93", Role.BODY: "33", Role.DANGER: "1;91", Role.SYSTEM: "93"},
}


def paint(text: str, role: Role, theme: ThemeName) -> str:
    """Envuelve una línea con su color y un reinicio; las líneas vacías quedan vacías."""
    if not text:
        return text
    return f"\x1b[{THEMES[theme][role]}m{text}{RESET}"

"""Cajas en UTF-8, CP437 y ASCII con el mismo ancho (R6.3)."""

from enum import StrEnum
from typing import NamedTuple

from telnet_tales.render.wrap import clip, visible_width

BOX_PADDING = 4  # Borde, espacio, espacio, borde: lo que una caja añade al texto.


class Charset(StrEnum):
    UTF8 = "utf8"
    CP437 = "cp437"
    ASCII = "ascii"


class BoxChars(NamedTuple):
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str


UNICODE_BOX = BoxChars("┌", "┐", "└", "┘", "─", "│")
ASCII_BOX = BoxChars("+", "+", "+", "+", "-", "|")
# CP437 usa los mismos glifos: todos existen en esa página, solo cambia la codificación.
BOXES = {Charset.UTF8: UNICODE_BOX, Charset.CP437: UNICODE_BOX, Charset.ASCII: ASCII_BOX}
ENCODINGS = {Charset.UTF8: "utf-8", Charset.CP437: "cp437", Charset.ASCII: "ascii"}


def encode_text(text: str, charset: Charset) -> bytes:
    # Un carácter que la página no tiene se sustituye por `?`: nunca rompe la sesión.
    return text.encode(ENCODINGS[charset], errors="replace")


def inner_width(lines: list[str], title: str, max_width: int) -> int:
    limit = max_width - BOX_PADDING
    widest = max(map(visible_width, [*lines, ""]))
    return min(limit, max(widest, visible_width(title) + 1))


def top_border(chars: BoxChars, title: str, inner: int) -> str:
    span = inner + 2
    if not title:
        return chars.top_left + chars.horizontal * span + chars.top_right
    label = f"{chars.horizontal} {clip(title, inner - 1)} "
    fill = chars.horizontal * (span - visible_width(label))
    return chars.top_left + label + fill + chars.top_right


def body_line(chars: BoxChars, line: str, inner: int) -> str:
    padding = " " * (inner - visible_width(line))
    return f"{chars.vertical} {line}{padding} {chars.vertical}"


def draw_box(lines: list[str], charset: Charset, title: str = "", max_width: int = 80) -> list[str]:
    """Dibuja una caja de a lo sumo `max_width` columnas; las líneas ya vienen ajustadas."""
    chars = BOXES[charset]
    inner = inner_width(lines, title, max_width)
    bottom = chars.bottom_left + chars.horizontal * (inner + 2) + chars.bottom_right
    body = [body_line(chars, line, inner) for line in lines]
    return [top_border(chars, title, inner), *body, bottom]

"""Ancho visible y ajuste de línea que entienden ANSI (R6.1). Cubre P9."""

import re
import unicodedata
from functools import partial
from itertools import chain

DEFAULT_COLUMNS = 80  # Ancho clásico de terminal; ninguna línea de salida lo supera.
MIN_COLUMNS = 2  # Un carácter ancho ocupa dos columnas: con menos no cabría ni uno.
ANSI_SEQUENCE = re.compile(r"\x1b\[[0-9;]*m")
TOKEN = re.compile(r"\x1b\[[0-9;]*m|.", re.DOTALL)
ZERO_WIDTH_CATEGORIES = frozenset({"Mn", "Me", "Cf"})


def strip_ansi(text: str) -> str:
    """Quita solo las secuencias de color (SGR); el texto no confiable usa `strip_escapes`."""
    return ANSI_SEQUENCE.sub("", text)


def strip_escapes(text: str) -> str:
    # El texto de la historia o del LLM nunca debe poder pintar ni mover el cursor.
    return strip_ansi(text).replace("\x1b", "")


def char_width(char: str) -> int:
    if unicodedata.category(char) in ZERO_WIDTH_CATEGORIES | {"Cc"}:
        return 0
    return 2 if unicodedata.east_asian_width(char) in "WF" else 1


def unit_width(unit: str) -> int:
    return 0 if ANSI_SEQUENCE.fullmatch(unit) else char_width(unit[0])


def visible_width(text: str) -> int:
    return sum(map(unit_width, split_units(text)))


def clean_char(token: str) -> str:
    """Tabuladores a espacio; el resto de caracteres de control se descarta."""
    if token == "\t":
        return " "
    return "" if unicodedata.category(token) == "Cc" else token


def attach(units: list[str], token: str) -> list[str]:
    """Los caracteres de ancho cero se pegan al anterior para no separarlos al partir."""
    if units and unit_width(token) == 0 and not ANSI_SEQUENCE.fullmatch(token):
        return [*units[:-1], units[-1] + token]
    return [*units, token]


def split_units(text: str) -> list[str]:
    tokens = [t if ANSI_SEQUENCE.fullmatch(t) else clean_char(t) for t in TOKEN.findall(text)]
    units: list[str] = []
    for token in filter(None, tokens):
        units = attach(units, token)
    return units


def hard_split(word: str, width: int) -> list[str]:
    """Parte una palabra más ancha que la línea, sin separar un carácter de su color."""
    chunks: list[str] = []
    current, used = "", 0
    for unit in split_units(word):
        if used + unit_width(unit) > width and current:
            chunks.append(current)
            current, used = "", 0
        current, used = current + unit, used + unit_width(unit)
    return [*chunks, current]


def place_word(lines: list[str], current: str, word: str, width: int) -> tuple[list[str], str]:
    if not word:
        return lines, current
    if visible_width(word) > width:
        pieces = hard_split(word, width)
        flushed = [*lines, current] if current else lines
        return [*flushed, *pieces[:-1]], pieces[-1]
    candidate = f"{current} {word}" if current else word
    if visible_width(candidate) <= width:
        return lines, candidate
    return [*lines, current], word


def wrap_line(line: str, width: int) -> list[str]:
    clean = "".join(split_units(line))
    if visible_width(clean) <= width:
        return [clean]  # Una línea que cabe no se toca: protege el arte ASCII.
    lines: list[str] = []
    current = ""
    for word in clean.split(" "):
        lines, current = place_word(lines, current, word, width)
    return [*lines, current]


def wrap_text(text: str, width: int = DEFAULT_COLUMNS) -> list[str]:
    """Ajusta por palabras; nunca devuelve una línea con ancho visible mayor que `width`."""
    if width < MIN_COLUMNS:
        raise ValueError(f"width must be at least {MIN_COLUMNS}")
    lines = text.splitlines() or [""]
    return list(chain.from_iterable(map(partial(wrap_line, width=width), lines)))


def clip(text: str, width: int) -> str:
    """Recorta a `width` columnas visibles (para títulos de caja); un hueco de 0 da vacío."""
    kept, used = "", 0
    for unit in split_units(text):
        used += unit_width(unit)
        if used > width:
            break
        kept += unit
    return kept

"""La única función de modelo de vista a bytes: ajuste, color, cajas y CRLF (R6.5)."""

from itertools import chain

from pydantic import Field

from telnet_tales.engine.models import FrozenModel
from telnet_tales.render.boxes import BOX_PADDING, Charset, draw_box, encode_text
from telnet_tales.render.theme import Role, ThemeName, paint
from telnet_tales.render.wrap import DEFAULT_COLUMNS, strip_escapes, wrap_text

CRLF = "\r\n"  # Telnet y xterm.js esperan CRLF; un LF suelto deja el cursor en la columna actual.
MIN_BOX_COLUMNS = 8  # Caja mínima: bordes, espacios y al menos un carácter ancho.


class Text(FrozenModel):
    role: Role
    text: str


class Box(FrozenModel):
    role: Role
    text: str
    title: str = ""


class RenderOptions(FrozenModel):
    theme: ThemeName = "green"
    charset: Charset = Charset.UTF8
    columns: int = Field(default=DEFAULT_COLUMNS, ge=MIN_BOX_COLUMNS, le=DEFAULT_COLUMNS)


Block = Text | Box


def render_text(block: Text, options: RenderOptions) -> list[str]:
    lines = wrap_text(strip_escapes(block.text), options.columns)
    return [paint(line, block.role, options.theme) for line in lines]


def render_box(block: Box, options: RenderOptions) -> list[str]:
    inner = options.columns - BOX_PADDING  # Hueco que dejan los bordes y los espacios.
    lines = wrap_text(strip_escapes(block.text), inner)
    boxed = draw_box(lines, options.charset, strip_escapes(block.title), options.columns)
    return [paint(line, block.role, options.theme) for line in boxed]


def render_block(block: Block, options: RenderOptions) -> list[str]:
    return render_box(block, options) if isinstance(block, Box) else render_text(block, options)


def render_lines(blocks: tuple[Block, ...], options: RenderOptions) -> list[str]:
    return list(chain.from_iterable(render_block(block, options) for block in blocks))


def render(blocks: tuple[Block, ...], options: RenderOptions) -> bytes:
    """Todo el texto del juego sale por aquí; Telnet y web reciben los mismos bytes (P14)."""
    lines = render_lines(blocks, options)
    return encode_text("".join(line + CRLF for line in lines), options.charset)

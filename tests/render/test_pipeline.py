"""Pruebas de la tubería: P9 (ancho), P14 base (mismos bytes siempre)."""

import re

from hypothesis import example, given, settings
from hypothesis import strategies as st

from telnet_tales.render.boxes import Charset
from telnet_tales.render.pipeline import Block, Box, RenderOptions, Text, render
from telnet_tales.render.theme import Role
from telnet_tales.render.wrap import visible_width

ANSI = re.compile(r"\x1b\[[0-9;]*m")
SGR_CODES = re.compile(r"\x1b\[([0-9;]*)m")
ALLOWED = {0, 1, *range(30, 38), *range(90, 98)}

options = st.builds(
    RenderOptions, theme=st.sampled_from(["green", "amber"]), charset=st.sampled_from(list(Charset))
)
roles = st.sampled_from(list(Role))
blocks = st.one_of(
    st.builds(Text, role=roles, text=st.text(max_size=300)),
    st.builds(Box, role=roles, text=st.text(max_size=300), title=st.text(max_size=60)),
)


def decode(data: bytes, charset: Charset) -> str:
    return data.decode("cp437" if charset == Charset.CP437 else "utf-8")


def test_text_ends_with_crlf_and_has_no_bare_newline() -> None:
    data = render((Text(role=Role.BODY, text="a\nb"),), RenderOptions())
    assert data == b"\x1b[32ma\x1b[0m\r\n\x1b[32mb\x1b[0m\r\n"


def test_story_text_cannot_inject_escape_sequences() -> None:
    data = render((Text(role=Role.BODY, text="\x1b[2Jboom"),), RenderOptions())
    assert b"\x1b[2J" not in data


def test_box_in_ascii_mode_is_pure_ascii() -> None:
    data = render(
        (Box(role=Role.SYSTEM, text="hello", title="BBS"),), RenderOptions(charset=Charset.ASCII)
    )
    assert ANSI.sub("", data.decode("ascii")).splitlines()[0].startswith("+-")


def test_same_input_gives_same_bytes_in_every_charset() -> None:
    view = (Text(role=Role.TITLE, text="x " * 100), Box(role=Role.BODY, text="y " * 90))
    for charset in Charset:
        assert render(view, RenderOptions(charset=charset)) == render(
            view, RenderOptions(charset=charset)
        )


@settings(max_examples=100, deadline=None)
@given(st.lists(blocks, max_size=4), options)
@example([Text(role=Role.BODY, text="漢" * 90)], RenderOptions())
def test_p9_p14_every_line_fits_and_output_is_deterministic(
    view: list[Block], opts: RenderOptions
) -> None:
    # P9: ancho visible <= 80 con cualquier texto, tema y juego de caracteres.
    # P14 base: la misma entrada da los mismos bytes, con CRLF y solo colores estándar.
    blocks_tuple = tuple(view)
    data = render(blocks_tuple, opts)
    assert data == render(blocks_tuple, opts)
    text = decode(data, opts.charset)
    assert text == "" or text.endswith("\r\n")
    assert "\n" not in text.replace("\r\n", "")
    for line in text.split("\r\n"):
        assert visible_width(line) <= 80
    codes = {int(part) for found in SGR_CODES.findall(text) for part in found.split(";") if part}
    assert codes <= ALLOWED

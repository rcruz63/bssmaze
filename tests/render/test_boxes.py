"""Pruebas de cajas: mismo ancho en UTF-8, CP437 y ASCII (R6.3)."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from telnet_tales.render.boxes import Charset, draw_box, encode_text
from telnet_tales.render.wrap import visible_width, wrap_text


def test_utf8_box_shape() -> None:
    assert draw_box(["hi"], Charset.UTF8) == ["┌────┐", "│ hi │", "└────┘"]


def test_ascii_box_uses_plain_characters() -> None:
    assert draw_box(["hi"], Charset.ASCII, "T") == ["+- T +", "| hi |", "+----+"]


def test_title_is_clipped_to_the_box() -> None:
    top = draw_box(["ab"], Charset.UTF8, "a very long title", max_width=10)[0]
    assert visible_width(top) <= 10


@pytest.mark.parametrize("charset", list(Charset))
def test_all_charsets_have_equal_widths(charset: Charset) -> None:
    box = draw_box(["one", "three"], charset, "t")
    assert {visible_width(line) for line in box} == {9}


def test_cp437_encodes_box_glyphs_as_single_bytes() -> None:
    assert encode_text("┌─┐", Charset.CP437) == bytes([0xDA, 0xC4, 0xBF])
    assert encode_text("é漢", Charset.ASCII) == b"??"


@settings(max_examples=100, deadline=None)
@given(st.text(max_size=300), st.text(max_size=100), st.sampled_from(list(Charset)))
def test_p9_boxes_never_exceed_80_columns(text: str, title: str, charset: Charset) -> None:
    # P9: una caja ajustada a 76 columnas mide como mucho 80, con cualquier juego de caracteres.
    lines = wrap_text(text, 76)
    for line in draw_box(lines, charset, title.replace("\n", " ")):
        assert visible_width(line) <= 80

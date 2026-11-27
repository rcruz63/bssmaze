"""Pruebas de ajuste de línea: P9 (ancho)."""

import re

import pytest
from hypothesis import example, given, settings
from hypothesis import strategies as st

from telnet_tales.render.wrap import clip, strip_ansi, strip_escapes, visible_width, wrap_text

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def test_ansi_does_not_count_as_width() -> None:
    assert visible_width("\x1b[1;92mhello\x1b[0m") == 5
    assert strip_ansi("\x1b[31mred\x1b[0m") == "red"


def test_wide_and_combining_characters() -> None:
    assert visible_width("漢字") == 4
    assert visible_width("e\u0301") == 1


def test_short_lines_and_blank_lines_are_untouched() -> None:
    art = "+--+\n|  |\n\n+--+"
    assert wrap_text(art) == ["+--+", "|  |", "", "+--+"]


def test_long_text_wraps_at_word_boundaries() -> None:
    lines = wrap_text("word " * 40, 20)
    assert all(visible_width(line) <= 20 for line in lines)
    assert " ".join(lines).split() == ["word"] * 40


def test_long_word_is_hard_split() -> None:
    assert wrap_text("x" * 25, 10) == ["x" * 10, "x" * 10, "x" * 5]


def test_ansi_word_is_not_cut_inside_a_sequence() -> None:
    lines = wrap_text("\x1b[1;92m" + "y" * 30 + "\x1b[0m", 10)
    assert all(visible_width(line) <= 10 for line in lines)
    assert all("\x1b" not in ANSI.sub("", line) for line in lines)


def test_escapes_and_controls_are_removed() -> None:
    assert strip_escapes("a\x1b[2Jb\x1b[31mc") == "a[2Jbc"
    assert wrap_text("a\x07b\x1bc") == ["abc"]


def test_tiny_width_is_refused_and_clip_works() -> None:
    with pytest.raises(ValueError, match="at least"):
        wrap_text("x", 1)
    assert clip("abcdef", 3) == "abc"


text_strategy = st.text(max_size=400)


@settings(max_examples=100, deadline=None)
@given(text_strategy, st.integers(min_value=2, max_value=80))
@example("漢" * 100, 3)
@example("\x1b[31m" + "z" * 200, 80)
def test_p9_every_wrapped_line_fits(text: str, width: int) -> None:
    # P9: para cualquier texto y ancho, ninguna línea supera el ancho visible.
    for line in wrap_text(text, width):
        assert visible_width(line) <= width
        assert len(ANSI.sub("", line)) <= width


def test_clip_respects_wide_characters_and_zero() -> None:
    assert clip("漢字", 3) == "漢"
    assert clip("abc", 0) == ""

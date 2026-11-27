"""Pruebas de temas: solo los 16 colores ANSI estándar (R6.2)."""

import re

from telnet_tales.render.theme import RESET, THEMES, Role, paint

ALLOWED_CODES = {1, *range(30, 38), *range(90, 98)}


def test_every_theme_maps_every_role_to_standard_codes() -> None:
    for codes in THEMES.values():
        assert set(codes) == set(Role)
        for value in codes.values():
            assert {int(part) for part in value.split(";")} <= ALLOWED_CODES


def test_paint_wraps_and_resets() -> None:
    assert paint("hi", Role.BODY, "green") == "\x1b[32mhi" + RESET


def test_empty_line_is_not_painted() -> None:
    assert paint("", Role.TITLE, "amber") == ""


def test_themes_differ() -> None:
    assert paint("x", Role.BODY, "green") != paint("x", Role.BODY, "amber")
    assert re.fullmatch(r"\x1b\[\d+(;\d+)*m", "\x1b[" + THEMES["amber"][Role.TITLE] + "m")

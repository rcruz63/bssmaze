"""Pruebas de i18n: P13 (mismas claves) y respaldo a inglés (R11)."""

import pytest

from telnet_tales.engine.actions import RejectionReason
from telnet_tales.render import i18n
from telnet_tales.render.i18n import UnknownMessageKeyError, load_catalog, translate


def test_p13_catalogs_have_identical_keys() -> None:
    # P13: en y es-ES comparten exactamente el mismo conjunto de claves.
    assert set(load_catalog("en")) == set(load_catalog("es-ES"))


def test_every_rejection_reason_has_a_message() -> None:
    keys = set(load_catalog("en"))
    assert {f"reject.{reason.value}" for reason in RejectionReason} <= keys


def test_translate_uses_the_requested_locale() -> None:
    assert translate("login.handle_prompt", "es-ES") == "Escribe tu alias:"
    assert translate("login.handle_prompt") == "Enter your handle:"


def test_missing_key_in_spanish_falls_back_to_english(monkeypatch: pytest.MonkeyPatch) -> None:
    spanish = {k: v for k, v in load_catalog("es-ES").items() if k != "no_carrier"}
    monkeypatch.setattr(
        i18n,
        "load_catalog",
        lambda locale: spanish if locale == "es-ES" else load_catalog.__wrapped__(locale),
    )
    assert i18n.translate("no_carrier", "es-ES") == "NO CARRIER"


def test_unknown_key_is_an_error() -> None:
    with pytest.raises(UnknownMessageKeyError):
        translate("nope.nothing")


def test_every_text_fits_80_columns() -> None:
    assert max(len(text) for text in load_catalog("en").values()) <= 78

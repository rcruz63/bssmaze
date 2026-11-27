"""Catálogos de textos de interfaz `en` y `es-ES` con respaldo a inglés (R11)."""

from functools import cache
from pathlib import Path
from typing import Literal

import yaml

Locale = Literal["en", "es-ES"]
DEFAULT_LOCALE: Locale = "en"
CATALOG_DIR = Path(__file__).parent / "catalogs"


class UnknownMessageKeyError(KeyError):
    """Una clave que no está ni en inglés es un error del programa, no del jugador."""


@cache
def load_catalog(locale: Locale) -> dict[str, str]:
    data = yaml.safe_load((CATALOG_DIR / f"{locale}.yaml").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"catalog {locale} must be a mapping of keys to texts")
    return {str(key): str(value) for key, value in data.items()}


def translate(key: str, locale: Locale = DEFAULT_LOCALE, **params: object) -> str:
    """Busca en `locale`, cae a `en` si falta la clave y rellena los parámetros."""
    text = load_catalog(locale).get(key)
    if text is None:
        text = load_catalog(DEFAULT_LOCALE).get(key)
    if text is None:
        raise UnknownMessageKeyError(key)
    return text.format(**params)

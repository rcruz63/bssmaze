# ADR 0002: Python 3.12+ con uv y tipado estricto

- Estado: aceptada
- Fecha: 2026-11-26

## Decisión
- Python 3.12 o superior, gestionado solo con **uv** (`uv sync`, `uv run`).
- Pydantic v2 para modelos y validación.
- **mypy --strict** como único verificador de tipos, con el plugin de Pydantic.
- ruff para lint y formato; pytest y hypothesis para pruebas.

## Motivos
- uv da entornos reproducibles con `uv.lock` y arranque rápido para el jurado.
- Pydantic valida las fronteras no fiables: red, salida del LLM, historias, guardados.
- mypy tiene el plugin de Pydantic más maduro; usar dos verificadores solo añade ruido.

## Alternativas
- pyright: más rápido, pero sin plugin equivalente para Pydantic.
- pip/poetry: más pasos de instalación.

## Consecuencias
Todas las instrucciones usan `uv run`. Cada función lleva anotaciones completas.

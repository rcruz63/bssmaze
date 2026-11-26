# ADR 0005: Narrador offline de respaldo y proveedor de LLM por defecto

- Estado: aceptada; el punto 3 (proveedor por defecto) fue reemplazado por la ADR 0006
- Fecha: 2026-11-26

## Decisión
1. `narrator/` define la interfaz `NarratorProvider` (narrar e interpretar).
2. Siempre existe un **narrador offline determinista** (plantillas más parser de verbos).
3. El proveedor LLM por defecto es **Anthropic Claude Haiku** mediante HTTPS, con la
   clave en `ANTHROPIC_API_KEY`. Otro proveedor compatible se añade implementando la interfaz.
4. Ante tiempo agotado (8 s), error o salida inválida, ese turno usa el narrador offline.

## Motivos
- Tests y CI sin red ni coste.
- La demo del jurado no depende de una cuota de API ni de la red.
- Haiku es rápido y barato, y sigue bien un esquema JSON estricto.
- Las claves nunca entran en el repositorio (`.env` ignorado, `.env.example` vacío).

## Alternativas
- Solo LLM: frágil y no determinista.
- Modelo local: instalación pesada para el jurado.

## Consecuencias
Hay que mantener dos narradores, pero el offline es pequeño y es también la base de las pruebas.

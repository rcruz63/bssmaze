# ADR 0006: Gemini como proveedor LLM por defecto

- Estado: aceptada (reemplaza el punto 3 de la ADR 0005)
- Fecha: 2026-11-26

## Contexto
La ADR 0005 elegía Claude Haiku. El equipo tiene clave de Gemini y no de Claude.

## Decisión
1. El proveedor por defecto es **Gemini**, con la biblioteca `google-genai`. Se añade
   con `uv add` en la tarea 13.1, no antes.
2. Opcional: **Vertex AI** con los créditos de un proyecto de GCP, con la misma biblioteca.
3. La clave va en `GEMINI_API_KEY` (o credenciales de GCP). Nunca en el repositorio.
4. Se mantienen la interfaz `NarratorProvider` y el narrador offline de la ADR 0005,
   incluido el límite de 8 s y el respaldo ante error o salida inválida.
5. Un `LLMBudgetGuard` limita las llamadas por sesión y por día; al llegar al tope,
   el turno usa el narrador offline.

6. Modelo por defecto: **`gemini-3.5-flash-lite`** (estable). Configurable con
   `TELNET_TALES_LLM_MODEL`. Verificado el 2026-11-26 (ver "Verificación").

## Verificación (2026-11-26)
- El valor anterior, `gemini-2.5-flash`, **no estaba verificado y está obsoleto**: la
  página de obsolescencias dice que desde el 2026-12-01 sus peticiones se redirigen a
  `gemini-3.5-flash-lite`. `gemini-2.5-flash-lite` sigue vivo pero solo para usuarios previos.
- `gemini-3.5-flash-lite` figura como estable: "el más rápido y barato de la serie 3.5"
  y es lo que la documentación recomienda para proyectos nuevos junto a Gemini 4 Hydrogen.
  Para narrar frases cortas basta y gasta menos crédito. Alternativa más potente: `gemini-3.8-flash`.
- SDK: `google-genai` 3.6.1 en PyPI (subido el 2026-11-18, Python >= 3.11). La guía rápida
  actual usa `from google import genai`, `genai.Client()` (lee `GEMINI_API_KEY`) y
  `client.interactions.create(model=..., input=...)` con `output_text`. La tarea 13.1
  debe volver a comprobar la llamada exacta antes de escribir código, y aislarla en un
  único adaptador pequeño para que un cambio del SDK no toque el resto.
- Fuentes: https://aistudio.google.com/docs/models,
  https://aistudio.google.com/docs/deprecations,
  https://aistudio.google.com/docs/quickstart, https://pypi.org/project/google-genai/
  (ai.google.dev redirige a aistudio.google.com).

## Motivos
- Es la clave que ya existe; los créditos de GCP cubren Gemini y el alojamiento.
- La interfaz aísla el proveedor: cambiarlo no toca `engine`.

## Consecuencias
Una dependencia nueva (`google-genai`) solo en la tarea 13.1. Los tests y la CI usan solo
el narrador offline y un cliente falso, sin red ni clave.

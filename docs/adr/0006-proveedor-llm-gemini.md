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

6. El id del modelo se lee **siempre** de la variable de entorno `GEMINI_MODEL` y nunca
   se escribe en el código. Así se cambia la configuración de Cloud Run sin redesplegar código.
   El valor inicial de `.env.example` es `gemini-3.5-flash-lite`, solo un valor por defecto
   que se puede sustituir. **No está verificado con una clave real.**
7. En la tarea 13.1 se debe comprobar el id exacto con la clave real, listando los modelos
   con el SDK (`client.models.list()`). El comando `python -m telnet_tales.narrator.list_models`
   imprime los ids disponibles. Si el modelo responde 404, se cambia `GEMINI_MODEL`, no el código;
   mientras tanto el turno usa el narrador offline.

## Verificación (2026-11-26): fuentes en conflicto, sin confirmar
Dos fuentes no coinciden y ninguna se ha probado con una clave real. El responsable del
proyecto cree que el id ligero estándar es `gemini-2.5-flash-lite` (o `gemini-2.5-flash`).
Una revisión anterior de la documentación afirmaba lo siguiente (no confirmado):
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
`GEMINI_MODEL` pasa a ser la única vía de elegir modelo (sustituye a `TELNET_TALES_LLM_MODEL`).
Una dependencia nueva (`google-genai`) solo en la tarea 13.1. Los tests y la CI usan solo
el narrador offline y un cliente falso, sin red ni clave.

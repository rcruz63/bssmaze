# ADR 0006: Proveedores LLM: Bedrock primario, Gemini de respaldo, offline al final

- Estado: aceptada; **reemplaza** la versión anterior de esta ADR (Gemini por defecto) y el
  punto 3 de la ADR 0005 (Claude Haiku por HTTPS)
- Fecha: 2026-11-26; reescrita el 2026-11-27

## Contexto
El despliegue pasa a AWS serverless (ADR 0010) y el usuario tiene créditos de AWS. Amazon
Bedrock queda en la misma cuenta, con permisos IAM en vez de una clave en un archivo.
La clave de Gemini sigue existiendo y sirve de respaldo.

## Decisión
1. Cadena de proveedores: **Bedrock -> Gemini -> narrador offline**. Cada eslabón solo se
   usa si está configurado y disponible; si falla (tiempo, error, salida inválida) pasa
   al siguiente, y el offline nunca falla.
2. La variable `LLM_PROVIDER` (`bedrock` | `gemini` | `offline`) elige el primer eslabón. La
   disponibilidad (credenciales, clave, tope de gasto) decide el resto de la cadena.
3. **Ningún id de modelo va en el código.** Bedrock lee `BEDROCK_MODEL_ID` y Gemini lee
   `GEMINI_MODEL`. Los valores de `.env.example` son solo ejemplos y **no están verificados**.
4. El id exacto se comprueba con la cuenta o la clave real en la tarea 13.1 (Bedrock) y 13.2
   (Gemini), con `python -m telnet_tales.narrator.list_models`, que lista los ids de ambos.
   Un 404 o un acceso denegado se arregla cambiando la variable, no el código; mientras tanto
   el turno usa el siguiente eslabón.
5. Adaptadores finos: `narrator/bedrock.py` (API Converse de `boto3`, importado de forma
   perezosa; `boto3` viene en el runtime de Lambda) y `narrator/gemini.py` (`google-genai`,
   dependencia añadida a `pyproject` solo en la tarea 13.2). El SDK queda aislado ahí.
6. Siguen la interfaz `NarratorProvider`, el límite de 8 s y el respaldo de la ADR 0005.
7. `LLMBudgetGuard` limita por sesión (`SESSION_LLM_CALL_CAP`) y por día
   (`DAILY_LLM_CALL_CAP`, contador atómico en DynamoDB, ADR 0009). Al llegar al tope, el
   turno usa el narrador offline.
8. Tests y CI: solo narrador offline y clientes falsos; nada de red.
9. El usuario debe **activar el acceso al modelo en Bedrock** en la región elegida.

## Nota de verificación de Gemini (2026-11-26): fuentes en conflicto, sin confirmar
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
  `client.interactions.create(model=..., input=...)` con `output_text`. La tarea 13.2
  debe volver a comprobar la llamada exacta antes de escribir código, y aislarla en un
  único adaptador pequeño para que un cambio del SDK no toque el resto.
- Fuentes: https://aistudio.google.com/docs/models,
  https://aistudio.google.com/docs/deprecations,
  https://aistudio.google.com/docs/quickstart, https://pypi.org/project/google-genai/
  (ai.google.dev redirige a aistudio.google.com).

## Motivos
- Bedrock usa los créditos y los permisos de AWS del mismo proyecto; Gemini evita depender de un solo proveedor.
- La interfaz aísla el proveedor: cambiarlo no toca `engine`.

## Consecuencias
`BEDROCK_MODEL_ID` y `GEMINI_MODEL` son la única vía de elegir modelo (sustituyen a
`TELNET_TALES_LLM_MODEL`). `google-genai` entra solo en la tarea 13.2 y `boto3` no se
empaqueta. Tareas 13.1 a 13.7.

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

## Motivos
- Es la clave que ya existe; los créditos de GCP cubren Gemini y el alojamiento.
- La interfaz aísla el proveedor: cambiarlo no toca `engine`.

## Consecuencias
Una dependencia nueva en la tarea 13.1. Los tests siguen usando solo el narrador
offline y un proveedor falso.

---
inclusion: always
---

# Code style

## Language
- Identifiers and file names: clear English, no cryptic abbreviations.
- **Code comments and everything under `/docs`: Spanish.** Use `#` comments.
- Comments explain **why** (business rule, formula, design reason), never what.
  Bad: `# suma 1 al contador`. Good: `# La tirada de suerte se repite una vez
  para no castigar al jugador por un fallo aislado.`
- UI strings are never hardcoded in logic: use the i18n catalog in `render/`.

## Size limits (hard, checked by `scripts/check_file_length.py`)
- File: **hard limit 200 lines**, soft target 150. Split before adding a feature.
- Function: 15-25 lines, one responsibility. Longer means extract.
- One responsibility per file. If you need "and" to describe it, split it.

## Zero nested loops (checked by `scripts/check_nested_loops.py`)
Forbidden in one function: `for` in `for`, `while` in `for`, comprehension with
two `for` clauses, comprehension inside a loop. Fix by:
1. extracting the inner loop into a named function;
2. building a dict indexed by id instead of scanning twice;
3. using a small tested domain utility (`chain.from_iterable`, `any`, `sum`).

## Typing
Every function fully annotated (`mypy --strict`). No `Any` unless at a
documented trust boundary. Prefer `Literal`, `StrEnum`, frozen models.

## Errors
Raise typed domain errors in `engine`; translate them at the edge (`server`).
Never swallow exceptions silently. Validate at trust boundaries: network
input, LLM output, story files, save files.

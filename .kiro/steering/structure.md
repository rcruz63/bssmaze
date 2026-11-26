---
inclusion: always
---

# Repository structure

```
src/telnet_tales/
  engine/    pure rules and state. No I/O, no LLM, no clock, no globals.
  narrator/  LLM client, prompts, offline fallback narrator, action parsing.
  stories/   loader + validator for story data (the data itself is in /stories).
  server/    Telnet and WebSocket layers, sessions, persistence, carrier drop I/O.
  render/    80-column formatter, ANSI themes, box drawing, baud throttle, i18n.
stories/     story data files (YAML). Content, not code.
tests/       mirrors src/ one to one (tests/engine/test_dice.py <-> engine/dice.py).
scripts/     repo-rule checkers used by hooks and `make check`
             (`validate_story_graph.py` + `story_validation/` for `stories/`).
docs/        Spanish documentation and ADRs (docs/adr/).
.kiro/       steering, specs, hooks. Always committed.
```

## Dependency direction (enforced in review)
`server -> narrator -> engine` and `server -> render`, `stories -> engine`.
`engine` imports nothing from the other packages. `render` never imports
`engine` state models except read-only views passed in as arguments.

## Naming
Files and identifiers in clear English with no cryptic abbreviations
(`hit_points`, not `hp`; `difficulty_class`, not `dc`). One concept per file.
Tests are named `test_<behavior>`.

# AGENTS.md

Instructions for any coding agent working in this repository. Full detail lives in
`.kiro/steering/` (always read `architecture-golden-rule.md` and `code-style.md`).

## Project
The Telnet Tales: AI-narrated text adventure imitating a 1980s Telnet BBS door game.
Kiroween 2026 (Resurrection). Game text in English; code comments and `/docs` in Spanish.

## Hard rules
1. **The LLM never mutates game state.** The Python engine (Pydantic v2) validates and applies everything.
2. Packages: `engine` (pure, no I/O, no LLM), `narrator`, `stories`, `server`, `render`.
3. Python 3.12+, **uv only**, `mypy --strict` on every function.
4. Files under **200 lines** (target 150). Functions 15-25 lines, one responsibility.
5. **Zero nested loops** (for-in-for, while-in-for, multi-`for` comprehensions).
6. Comments in Spanish with `#`, explaining WHY. Identifiers in clear English.
7. Output limited to 80 columns, 16 ANSI colors, baud throttle only in the output layer.
8. Every `engine/` change needs hypothesis property tests plus pytest unit tests.
9. A task is done only if `make check` passes. Never tick `tasks.md` otherwise.
10. Never add `.kiro` to `.gitignore`. Never commit secrets.
11. After every milestone (task done, ADR, notable decision) and every hypothesis
    failure, append a short entry to `DEVLOG.md` (`.kiro/steering/devlog.md`).

## Commands
`uv sync` | `make check` | `uv run pytest` | `uv run ruff check .` | `uv run mypy`

## Where to look
- Spec: `.kiro/specs/telnet-tales/` (requirements, design, tasks)
- Hooks: `.kiro/hooks/` backed by `scripts/` (`run-tests-on-save`, `validate-story-graph`, ...)
- Story vocabulary: node `id`, `exits`, `target_id`, `is_ending`
- Build diary for judges: `DEVLOG.md`
- Game rules: `docs/game-design.es.md`; decisions: `docs/adr/`

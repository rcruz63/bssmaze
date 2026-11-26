---
inclusion: always
---

# Testing and definition of done

## Required tests
- **Every change in `engine/` needs both** a hypothesis property test and a
  pytest unit test. Properties come from the "Correctness properties" list in
  `.kiro/specs/telnet-tales/design.md`; cite the property id in a comment.
- Every other package needs unit tests; the renderer needs a width property.
- Tests are deterministic: seeded RNG, fake clock, no network, no real LLM.
  The offline narrator is the default in tests.
- Test files mirror source files: `tests/engine/test_dice.py`.

## A task is done only when ALL of these pass
```
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
make scripts        # file length, nested loops, .kiro not ignored, story graph
```
`make check` runs them all. **Never tick a checkbox in `tasks.md` while any of
them fails.** If something cannot run, the task stays open and you say why.

## Hypothesis settings
Use `@settings(max_examples=100, deadline=None)` for engine properties. A
failing example must be pinned with `@example(...)` before fixing the bug.

## Test hygiene
No sleeps, no real sockets except loopback in `tests/server`, no files outside
`tmp_path`, no environment reads without `monkeypatch`.

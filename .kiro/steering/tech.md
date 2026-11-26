---
inclusion: always
---

# Technology stack

- **Python 3.12+**, managed only with **uv** (`uv sync`, `uv run ...`). Never
  use `pip install` or a bare `python` command in instructions.
- **Pydantic v2** for every data model (state, actions, story nodes).
- **PyYAML** for story files (`stories/*.yaml`), always validated by Pydantic.
- **pytest** + **hypothesis** (property-based tests).
- **ruff** (lint + format) and **mypy --strict** (single type checker, chosen
  because the `pydantic.mypy` plugin is mature; do not add pyright).
- **Telnet server:** `telnetlib3` (asyncio, ISC license, added in task 8) behind
  a thin `server/` adapter (see ADR 0003). **Web terminal:** WebSocket + xterm.js (ADR 0004).
- **LLM:** provider interface in `narrator/`; default Anthropic Claude Haiku via
  HTTPS, plus an offline deterministic narrator (ADR 0005).
- Secrets only in environment variables (`.env`, never committed).
  `.env.example` lists the names.

## Commands
| Goal | Command |
|------|---------|
| Install | `uv sync` |
| Everything | `make check` |
| Tests | `uv run pytest` |
| Lint | `uv run ruff check .` and `uv run ruff format --check .` |
| Types | `uv run mypy` |
| Repo rules | `make scripts` |

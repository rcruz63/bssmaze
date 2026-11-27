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
- **Telnet server (local only, not deployed):** `telnetlib3` (asyncio, ISC license, added in
  task 8) behind a thin `server/` adapter (ADR 0003).
- **Web terminal:** static xterm.js page calling `POST /api/command` on an API Gateway
  HTTP API (no WebSocket, ADR 0004, 0010). The browser paces bytes to the baud rate.
- **Hosting (ADR 0010):** serverless AWS: S3 + CloudFront, HTTP API, Lambda (Python 3.12,
  arm64, plain `.zip` built with uv, `boto3` from the runtime), DynamoDB single table
  (on demand, TTL), AWS SAM (`infra/template.yaml`, `sam deploy`). Alternatives kept in
  the ADRs: Cloud Run, Lightsail.
- **LLM chain (ADR 0006):** provider interface in `narrator/`; Amazon Bedrock first
  (`BEDROCK_MODEL_ID`), Gemini fallback (`google-genai`, `GEMINI_MODEL`, added to
  `pyproject` only in task 13.2), offline deterministic narrator last. `LLM_PROVIDER`
  picks the start. Model ids come only from env and are verified with the real account or
  key (`list_models`). Per-session and daily call caps fall back to offline.
  Tests and CI use only the offline narrator or fake clients: no network.
- **State (ADR 0009):** `StateStore` = `SaveStore` + `DailyBudget` + `LoginAttempts`;
  `DynamoStateStore`, `MemoryStore`, `FileStore`.
- Telnet and web are thin transports over one `render/` pipeline and one session facade (ADR 0008).
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
| Repo rules | `make scripts` (file length, nested loops, `.kiro`, story graph) |

# The Telnet Tales

> Summoning the ghost of 1980s dial-up BBS doors to run AI-powered interactive
> fiction. Connect at 2400 baud, explore ASCII labyrinths, and pray the SysOp
> doesn't drop your carrier mid-combat.

Kiroween 2026 entry, category **Resurrection**. Built between 30 Oct and 4 Dec 2026
with [Kiro](https://kiro.dev). No pre-existing code was reused.

**Status:** foundation committed (steering, specs, hooks, tooling). Game code
follows the plan in [`tasks.md`](.kiro/specs/telnet-tales/tasks.md).

_Screenshot: coming with the demo (task 16.1)._

## The idea
A text adventure that behaves like a Telnet BBS door game: login screen, SysOp
bulletins, 80 columns, green or amber phosphor, simulated modem speed. An LLM
narrates and understands free-text commands, but **the Python engine is the only
thing that can change the game**. The LLM proposes, the engine disposes.

Signature feature: **carrier drop.** The SysOp may cut your line mid-combat. Your
state is saved; call back and the fight resumes.

## How Kiro was used
| Kiro feature | What we did | Where |
|---|---|---|
| **Specs** | EARS requirements, design with 13 correctness properties for property tests, ordered tasks with day markers | [`.kiro/specs/telnet-tales/`](.kiro/specs/telnet-tales/) |
| **Steering** | Always-on product/tech/structure, architecture golden rule, code style, retro terminal rules, testing, git; `fileMatch` for `engine/**`; manual submission checklist | [`.kiro/steering/`](.kiro/steering/) |
| **Hooks** | `run-tests-on-save` (ruff fix + pytest), format + file-length, no-nested-loops, `validate-story-graph`, engine test reminder, task gate (`make check`), `.kiro`-not-ignored guard | [`.kiro/hooks/`](.kiro/hooks/) |
| **Strategy** | Vertical slice first (engine, offline narrator, renderer, Telnet) before the LLM | [`tasks.md`](.kiro/specs/telnet-tales/tasks.md) |
| **Agent rules** | Same rules for any agent | [`AGENTS.md`](AGENTS.md) |

Hooks are backed by real scripts with tests: [`scripts/`](scripts/).

## Architecture
```mermaid
flowchart LR
  Client[Telnet / Web client] --> Server[server]
  Server --> Narrator[narrator: LLM or offline]
  Server --> Engine[engine: rules + state]
  Server --> Render[render: 80 cols, ANSI, baud]
  Narrator -->|ProposedAction| Engine
  Stories[stories: YAML] --> Engine
```
Details: [design.md](.kiro/specs/telnet-tales/design.md). Spanish docs and ADRs are in [`docs/`](docs/).

## Quickstart
```bash
uv sync
make check          # ruff, mypy --strict, pytest + hypothesis, repo rules
cp .env.example .env   # optional: add GEMINI_API_KEY; works offline without it
```
Planned: `uv run telnet-tales` then `telnet localhost 2323` (or `nc localhost 2323`),
and a web terminal at `http://localhost:8080`.

## Demo and LLM
Default LLM: Gemini (optional Vertex AI), with call caps and an offline fallback.
The public demo is the web terminal only, behind a login (credentials in the
Devpost testing instructions), on Google Cloud Run. Real Telnet runs locally and
in the video. AWS is the documented alternative. See ADRs 0006 and 0007.

## Rules in one glance
- The LLM never mutates state; every action is validated by the engine.
- Files under 200 lines, zero nested loops, strict typing: enforced by scripts and hooks.
- Comments and `/docs` in Spanish; game text in English.

## License
[MIT](LICENSE) (c) The Telnet Tales contributors.

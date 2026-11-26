# Implementation plan: The Telnet Tales

Rule: a task is ticked only when `make check` passes (pytest, ruff check, ruff
format --check, mypy, file length, nested loops, .kiro not ignored). Every
engine task also adds hypothesis + pytest tests. Files < 200 lines.

Plan: today is Thu 26 Nov. Target feature-complete **Tue 1 Dec**. Wed 2 - Fri 4
Dec is buffer for submission (deadline 4 Dec).

## Day 0 - Thu 26 Nov: foundation
- [x] 0. Bootstrap repo, steering, hooks, spec, docs, tooling (R12)
  - Verify: `make check`

## Day 1 - Fri 27 Nov: engine, story, offline narrator (runnable slice)
- [ ] 1. Engine core models and seeded dice
  - [ ] 1.1 `engine/models.py`: Stats, Player, GameState (frozen) (R1.1)
  - [ ] 1.2 `engine/dice.py`: seeded RNG, `roll_d20`, `check` (R1.2, R1.3) - P1, P2
  - Verify: `uv run pytest tests/engine && make check`
- [ ] 2. Actions and rules
  - [ ] 2.1 `engine/actions.py`: ProposedAction, allow-list, Rejection (R5.1, R5.2) - P7
  - [ ] 2.2 `engine/rules.py`: move, look, take, inventory with validation (R1.5) - P3, P4, P5
  - Verify: `make check`
- [ ] 3. Story loader and validator
  - [ ] 3.1 `stories/schema.py`: StoryNode, Exit, Requirement, Encounter (R2.1)
  - [ ] 3.2 `stories/loader.py`: YAML load, aggregated errors (R2.3)
  - [ ] 3.3 `stories/graph.py`: reachability, dead ends, unknown refs (R2.2) - P6
  - Verify: `make check`
- [ ] 4. "The Haunted Maze" story data
  - [ ] 4.1 `stories/haunted_maze.yaml` with 12-15 nodes, 2 encounters, 1 key item (R2.4)
  - [ ] 4.2 Test: the shipped story validates and is winnable
  - Verify: `make check`
- [ ] 5. Offline narrator and command parser
  - [ ] 5.1 `narrator/provider.py`: Protocol, NarrationContext (R4.1, R4.2)
  - [ ] 5.2 `narrator/offline.py`: template narration + keyword parser (R4.5) - P8
  - Verify: `make check`

## Day 2 - Sat 28 Nov: renderer, Telnet server, baud
- [ ] 6. Renderer
  - [ ] 6.1 `render/wrap.py`: ANSI-aware visible width and word wrap (R6.1) - P9
  - [ ] 6.2 `render/theme.py`: green/amber role-to-color mapping (R6.2)
  - [ ] 6.3 `render/boxes.py`: UTF-8, CP437, ASCII boxes (R6.3)
  - [ ] 6.4 `render/i18n.py` + `en.yaml`/`es-ES.yaml` catalogs (R11) - P13
  - Verify: `make check`
- [ ] 7. Session loop and BBS flow
  - [ ] 7.1 `server/session.py`: login, handle, bulletins, menu, turn loop (R8.1)
  - [ ] 7.2 Call time limit and `NO CARRIER` (R8.2, R8.3)
  - Verify: `make check` (session tested with in-memory streams)
- [ ] 8. Telnet server
  - [ ] 8.1 `server/telnet.py`: telnetlib3 shell adapter (add dependency with `uv add telnetlib3`), ADR 0003 (R7.1)
  - [ ] 8.2 Session cap and idle timeout (R7.3)
  - [ ] 8.3 Loopback integration test with `asyncio.open_connection`
  - Verify: `make check`; manual `nc localhost 2323`
- [ ] 9. Baud throttle
  - [ ] 9.1 `render/throttle.py` with injectable clock (R6.4) - P10
  - [ ] 9.2 Wire into server writer, config via env
  - Verify: `make check`

## Day 3 - Sun 29 Nov: combat, LLM, carrier drop
- [ ] 10. Combat
  - [ ] 10.1 `engine/combat.py`: rounds, attack, flee (R3) - P4
  - [ ] 10.2 Story encounters wired to combat state
  - Verify: `make check`
- [ ] 11. Save and resume
  - [ ] 11.1 `server/saves.py`: JSON per handle, validation, `.bad` quarantine (R10) - P11
  - Verify: `make check`
- [ ] 12. Carrier drop
  - [ ] 12.1 `engine/carrier.py`: drop decision from engine RNG (R9.1, R9.4)
  - [ ] 12.2 Server: save, in-fiction messages, close; resume on reconnect (R9.2, R9.3) - P12
  - Verify: `make check`; forced-drop integration test
- [ ] 13. LLM narrator
  - [ ] 13.1 `narrator/anthropic.py`: HTTPS client, timeout, key from env (R4.3)
  - [ ] 13.2 `narrator/prompts.py`: bounded context, delimited player text (R5.4)
  - [ ] 13.3 `narrator/guard.py`: JSON parse, schema, fallback to offline (R4.3, R5.5) - P8
  - [ ] 13.4 Fake-provider tests: timeout, garbage, injection strings
  - Verify: `make check`

## Day 4 - Mon 30 Nov: web terminal
- [ ] 14. Web terminal
  - [ ] 14.1 `server/web.py`: WebSocket endpoint sharing the session loop (R7.2)
  - [ ] 14.2 Static page with xterm.js (vendored, license noted), CRT styling
  - [ ] 14.3 Deployment recipe (Dockerfile or Fly.io/Render), public URL
  - Verify: `make check`; open the URL in a browser

## Day 5 - Tue 1 Dec: polish, demo, submission prep
- [ ] 15. Polish
  - [ ] 15.1 SysOp bulletins, ANSI title screen, ASCII maze map art
  - [ ] 15.2 Playtest full story on 2400 baud; fix pacing
- [ ] 16. Submission assets
  - [ ] 16.1 README: screenshots, demo URL, Kiro usage section (R12.4)
  - [ ] 16.2 Demo video script and recording (< 3 min)
  - [ ] 16.3 Blog post and social post draft (#KiroweenHackathon26)
  - [ ] 16.4 Walk `#submission-checklist` steering file
  - Verify: `make check` on a fresh clone

## Buffer - Wed 2 to Fri 4 Dec
Bugs, video re-take, publishing posts, submit by Thu 3 Dec to leave margin.

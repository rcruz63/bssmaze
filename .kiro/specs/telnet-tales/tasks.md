# Implementation plan: The Telnet Tales

Rule: a task is ticked only when `make check` passes (pytest, ruff check, ruff
format --check, mypy, file length, nested loops, .kiro not ignored). Every
engine task also adds hypothesis + pytest tests. Files < 200 lines.
Every task also ends with `DEVLOG entry added` (see `.kiro/steering/devlog.md`):
append a short entry to `DEVLOG.md`, and one for every hypothesis failure found.

Plan: today is Thu 26 Nov. Target feature-complete **Tue 1 Dec**. Wed 2 - Fri 4
Dec is buffer for submission (deadline 4 Dec).

## Day 0 - Thu 26 Nov: foundation
- [x] 0. Bootstrap repo, steering, hooks, spec, docs, tooling (R12)
  - [x] 0.1 `scripts/validate_story_graph.py` + hooks `run-tests-on-save`, `validate-story-graph`; vocabulary `target_id` / `is_ending` (R2.2, R12.2)
  - [x] 0.2 Align spec (Cloud Run, shared render pipeline, Gemini narrator), `DEVLOG.md`, steering `devlog.md`, hook `devlog-reminder` (R4.6, R6.5, R7.5, R13)
  - [x] 0.3 Pivot spec and docs to serverless AWS: ADR 0006/0007/0009/0010, R4/R6/R7/R10/R13, `design-aws.md`, tasks (ADR 0010)
  - [x] DEVLOG entry added
  - Verify: `make check`

## Day 1 - Fri 27 Nov: engine, story, offline narrator (runnable slice)
- [x] 1. Engine core models and seeded dice
  - [x] 1.1 `engine/models.py`: Stats, Player, GameState (frozen) (R1.1)
  - [x] 1.2 `engine/dice.py`: seeded RNG, `roll_d20`, `check` (R1.2, R1.3) - P1, P2
  - [x] DEVLOG entry added
  - Verify: `uv run pytest tests/engine && make check`
- [x] 2. Actions and rules
  - [x] 2.1 `engine/actions.py`: ProposedAction, allow-list, Rejection (R5.1, R5.2) - P7
  - [x] 2.2 `engine/rules.py`: move, look, take, inventory with validation (R1.5) - P3, P4, P5
  - [x] DEVLOG entry added
  - Verify: `make check`
- [ ] 3. Story loader and validator
  - [ ] 3.1 `stories/schema.py`: StoryNode, Exit, Requirement, Encounter (R2.1)
  - [ ] 3.2 `stories/loader.py`: YAML load, aggregated errors (R2.3)
  - [ ] 3.3 `stories/graph.py`: reachability, dead ends, unknown refs (R2.2) - P6
  - [ ] DEVLOG entry added
  - Verify: `make check`
- [ ] 4. "The Haunted Maze" story data
  - [ ] 4.1 `stories/haunted_maze.yaml` with 12-15 nodes, 2 encounters, 1 key item (R2.4)
  - [ ] 4.2 Test: the shipped story validates and is winnable
  - [ ] DEVLOG entry added
  - Verify: `make check`
- [ ] 5. Offline narrator and command parser
  - [ ] 5.1 `narrator/provider.py`: Protocol, NarrationContext (R4.1, R4.2)
  - [ ] 5.2 `narrator/offline.py`: template narration + keyword parser (R4.5) - P8
  - [ ] DEVLOG entry added
  - Verify: `make check`

## Day 2 - Sat 28 Nov: smoke deploy, renderer, session facade
- [ ] S1. Smoke deploy (do this first; ADR 0010 fallback decision depends on it)
  - [x] S1.1 User: `aws configure sso` (or a profile) in their own terminal, pick the region, enable Bedrock model access (never in the repo)
  - [x] S1.2 `infra/template.yaml` minimal: hello-world Lambda + HTTP API `POST /api/command` + DynamoDB table + S3 + CloudFront with `/api/*` routing (R7.2, R13.8)
  - [ ] S1.3 `sam build && sam deploy --guided`; open the CloudFront URL, call `/api/command`, write and read one DynamoDB item
  - [x] S1.4 Note cold start time and any blocker in DEVLOG; if blocked, plan the Lightsail fallback (ADR 0010)
  - [x] DEVLOG entry added
  - Verify: `curl` the CloudFront `/api/command` URL returns the hello-world JSON
- [ ] 6. Renderer
  - [ ] 6.1 `render/wrap.py`: ANSI-aware visible width and word wrap (R6.1) - P9
  - [ ] 6.2 `render/theme.py`: green/amber role-to-color mapping (R6.2)
  - [ ] 6.3 `render/boxes.py`: UTF-8, CP437, ASCII boxes (R6.3)
  - [ ] 6.5 `render/pipeline.py`: the only view-model -> bytes function (wrap, color, boxes, CRLF) (R6.5) - P14 base
  - [ ] 6.4 `render/i18n.py` + `en.yaml`/`es-ES.yaml` catalogs (R11) - P13
  - [ ] DEVLOG entry added
  - Verify: `make check`
- [ ] HUMAN GATE G1: STOP. Do not start any task below until the user confirms in chat. Playtest feel: first playable turn.
- [ ] 7. Session facade, auth and HTTP schema (transport-neutral)
  - [ ] 7.1 `server/session.py`: facade `handle_command(store, request) -> response`, stateless per command: login, handle, bulletins, menu, turn (R8.1, R7.9)
  - [ ] 7.2 Call time limit counted in the token and `NO CARRIER` (R8.2, R8.3)
  - [ ] 7.3 `server/transport.py`: `Transport` Protocol (read_line, write_bytes, close) used only by the local Telnet adapter (R7.5)
  - [ ] 7.4 `server/auth.py`: credentials from env, `hmac.compare_digest`, HMAC-signed token with expiry, lockout via `LoginAttempts`, injectable clock (R13.1-R13.4, R13.7) - P16
  - [ ] 7.5 `server/schema.py`: `CommandRequest` / `CommandResponse` (`extra="forbid"`, 200-char text cap) (R7.8)
  - [ ] DEVLOG entry added
  - Verify: `make check` (facade tested with `MemoryStore`, no sockets)
- [ ] 8. Telnet server (local only, never deployed, ADR 0010)
  - [ ] 8.1 `server/telnet.py`: telnetlib3 shell adapter (add dependency with `uv add telnetlib3`), ADR 0003 (R7.1)
  - [ ] 8.2 Session cap and idle timeout (R7.3)
  - [ ] 8.3 Loopback integration test with `asyncio.open_connection`
  - [ ] DEVLOG entry added
  - Verify: `make check`; manual `nc localhost 2323`
- [ ] 9. Baud throttle (local Telnet; the browser paces itself in 14.4)
  - [ ] 9.1 `render/throttle.py` with injectable clock (R6.4, R6.6) - P10
  - [ ] 9.2 Wire into the Telnet writer, config via env; test that throttled and unthrottled bytes are equal (R6.6)
  - [ ] DEVLOG entry added
  - Verify: `make check`

## Day 3 - Sun 29 Nov: combat, state stores, LLM chain, carrier drop
Decision point: if the serverless smoke deploy (S1) still fails today, switch to the Lightsail fallback (ADR 0010).
- [ ] HUMAN GATE G2: STOP. Do not start combat until the user confirms in chat. Combat balance.
- [ ] 10. Combat
  - [ ] 10.1 `engine/combat.py`: rounds, attack, flee (R3) - P4
  - [ ] 10.2 Story encounters wired to combat state
  - [ ] DEVLOG entry added
  - Verify: `make check`
- [ ] 11. State stores and resume
  - [ ] 11.1 `server/saves.py`, `server/budget_store.py`, `server/login_attempts.py`: tiny Protocols `SaveStore` (load, save, delete), `DailyBudget`, `LoginAttempts`; `server/state.py`: `StateStore` composition (R10.4) - ADR 0009
  - [ ] 11.2 `SaveGame` and `MemoryStore`, `FileStore`: JSON per handle, validation, `.bad` quarantine, in-memory atomic budget (R10.1-R10.3, R10.5) - P11, P15, P16, P17
  - [ ] DEVLOG entry added
  - Verify: `make check`

- [ ] 12. Carrier drop
  - [ ] 12.1 `engine/carrier.py`: drop decision from engine RNG (R9.1, R9.4)
  - [ ] 12.2 Server: save, in-fiction messages, close; resume on reconnect (R9.2, R9.3) - P12
  - [ ] DEVLOG entry added
  - Verify: `make check`; forced-drop integration test
- [ ] 13. LLM narrator chain (Bedrock -> Gemini -> offline; ADR 0006)
  - [ ] 13.1 `narrator/bedrock.py`: Converse API through lazy `boto3`, model only from env `BEDROCK_MODEL_ID`, 8 s timeout (R4.3, R4.6, R4.8, R4.10)
    - Verify the exact model id with the real account (`list_foundation_models` / inference profiles) before relying on any example; access denied or 404 means change the env var, not code
    - `narrator/list_models.py`: `python -m telnet_tales.narrator.list_models` prints available Bedrock and Gemini ids (R4.9); fake clients in tests, no network
  - [ ] 13.2 `narrator/gemini.py`: `uv add google-genai` (first and only place it enters `pyproject`), model only from env `GEMINI_MODEL` (example not verified), `GEMINI_API_KEY`; re-check the SDK call against the docs (R4.6, R4.8, R4.10) - ADR 0006
    - Verify the exact id with the real key (`client.models.list()`); a 404 means change `GEMINI_MODEL`, not code
  - [ ] 13.3 `narrator/prompts.py`: bounded context, delimited player text (R5.4)
  - [ ] 13.4 `narrator/guard.py`: JSON parse, schema, fallback (R4.3, R5.5) - P8
  - [ ] 13.5 `narrator/chain.py`: `LLM_PROVIDER` plus availability; Bedrock -> Gemini -> offline (R4.6, R4.10)
  - [ ] 13.6 Fake-provider and fake Bedrock/Gemini client tests: timeout, garbage, injection strings, no credentials, no network (R4.7)
  - [ ] 13.7 `narrator/budget.py`: per-session cap (token counter) and daily cap through `DailyBudget`, fallback to offline (R13.5, R13.6) - P15
  - [ ] DEVLOG entry added
  - Verify: `make check`

## Day 4 - Mon 30 Nov: web terminal and AWS deploy
- [ ] 14. Web terminal and serverless deploy (ADR 0010)
  - [ ] 14.1 `server/dynamo_state.py`: `DynamoStateStore` on one table; `ConditionExpression` budget, lockout with TTL, lazy `boto3`; fake client tests (R10.5, R13.3, R13.5) - P15, P16, P17
  - [ ] 14.2 `server/lambda_handler.py` (thin): parse `CommandRequest`, call the facade, return `CommandResponse`; client IP from the HTTP API event (R7.2, R7.5, R7.9)
  - [ ] 14.3 `make package`: `.zip` with `uv pip install --target --python-platform aarch64-manylinux2014` (pydantic, pyyaml; no boto3), plus `src/` and `stories/`; check the size (R13.8)
  - [ ] 14.4 `static/`: xterm.js (vendored, license noted), CRT CSS, `terminal.js` with client-side baud pacing, fake telnet banner, `NO CARRIER` on `carrier_dropped` (R6.4, R7.2, R7.7)
  - [ ] 14.5 `infra/template.yaml`: Lambda (arm64, reserved concurrency), HTTP API, DynamoDB (PAY_PER_REQUEST, TTL `ttl`), S3, CloudFront with `/api/*`, SSM or env for secrets (R13.8)
  - [ ] 14.6 AWS Budgets alert in the template; check the daily cap works with a forced fallback (R13.5, R13.8)
  - [ ] 14.7 `tests/server/test_transport_parity.py`: same seed and script through the Telnet adapter and the Lambda handler, equal bytes, plus a golden file (R7.6) - P14
  - [ ] 14.8 Check the CRT CSS/JS and baud pacing never alter bytes: no text transform in `static/` (R7.7)
  - [ ] 14.9 `docs/despliegue-aws.md` (Spanish): `sam build`, `sam deploy`, credentials as a user action, region, Bedrock access; README demo URL (R13.8)
  - [ ] HUMAN GATE G4: STOP. No AWS deploy beyond the smoke stack, publishing commits to a remote, secret or API key use, or spending until the user confirms in chat.
  - [ ] 14.10 `sam deploy` to the real account; verify `BEDROCK_MODEL_ID` with `list_models`; credentials into the Devpost testing-instructions field (not in the repo)
  - [ ] DEVLOG entry added
  - Verify: `make check`; open the CloudFront URL in a browser

## Day 5 - Tue 1 Dec: polish, demo, submission prep
- [ ] HUMAN GATE G3: STOP. No story or tone rewrite beyond the draft until the user confirms in chat.
- [ ] 15. Polish
  - [ ] 15.1 SysOp bulletins, ANSI title screen, ASCII maze map art
  - [ ] 15.2 Playtest full story on 2400 baud; fix pacing
  - [ ] DEVLOG entry added
- [ ] 16. Submission assets
  - [ ] 16.1 README: screenshots, demo URL, Kiro usage section (R12.4)
  - [ ] HUMAN GATE G5: STOP. No final demo video or submission until the user confirms in chat.
  - [ ] 16.2 Demo video script and recording (< 3 min)
  - [ ] 16.3 Blog post and social post draft (#KiroweenHackathon26)
  - [ ] 16.4 Walk `#submission-checklist` steering file (demo credentials in Devpost, Telnet shown in video)
  - [ ] DEVLOG entry added
  - Verify: `make check` on a fresh clone

## Buffer - Wed 2 to Fri 4 Dec
Bugs, video re-take, publishing posts, submit by Thu 3 Dec to leave margin.

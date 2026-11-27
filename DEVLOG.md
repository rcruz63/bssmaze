# DEVLOG - The Telnet Tales

Build diary for the Kiroween 2026 judges (category **Resurrection**). It is the raw
material for the Devpost text. Entries are short and honest: only what exists today.
Rules for keeping it current: [`.kiro/steering/devlog.md`](.kiro/steering/devlog.md).

## Inspiration
Summoning the ghost of 1980s dial-up BBS doors to run AI-powered interactive
fiction. Connect at 2400 baud, explore ASCII labyrinths, and pray the SysOp doesn't
drop your carrier mid-combat. BBS door games were small, strange and social; an LLM
can give them a narrator again, if something strict keeps the rules fair.

## What it does
Planned (nothing playable yet): a Telnet BBS door game, "The Haunted Maze". You dial
in, pick a handle, read SysOp bulletins and enter a door menu. An LLM narrates and
reads free-text commands; the Python engine alone changes the game. Signature
feature: the **carrier drop**. The engine may cut your line mid-combat, saves the
state, and the same handle resumes the same round. Telnet and a web terminal show
the same bytes.

## How we built it
- Spec-driven: EARS requirements, a design with 17 correctness properties, and
  ordered tasks ([`.kiro/specs/telnet-tales/`](.kiro/specs/telnet-tales/)).
- Golden rule: the LLM never mutates state ([ADR 0001](docs/adr/0001-llm-nunca-modifica-el-estado.md)).
  Model output is a `ProposedAction` that the engine validates or rejects.
- Python 3.12, uv, Pydantic v2, `mypy --strict`, pytest + hypothesis.
- Narrator: a chain Amazon Bedrock, then Gemini, then a deterministic offline narrator
  that needs no key and runs all tests ([ADR 0006](docs/adr/0006-proveedor-llm-gemini.md)).
- Public demo: web terminal on serverless AWS (S3, CloudFront, HTTP API, Lambda,
  DynamoDB) behind a BBS-style login, with call caps that protect the credit
  ([ADR 0010](docs/adr/0010-serverless-aws.md), [ADR 0007](docs/adr/0007-demo-publica-cloud-run.md)).
- One render pipeline and one session facade under both transports
  ([ADR 0008](docs/adr/0008-dos-transportes-una-tuberia.md)).

## Challenges we ran into
Expected, not yet met: keeping an LLM useful while it has no power over state;
80 columns with ANSI colors; making a random carrier drop testable. Real failures
will be written in the Log, with the property-test counterexample.
Already hit: Gemini model ids from our notes conflict and are unverified; ids now come
only from `GEMINI_MODEL` and `BEDROCK_MODEL_ID`, and are checked with a list command.

## Accomplishments that we're proud of
So far, only the foundation: steering, spec, hooks that run real scripts with tests,
and a story-graph validator. No game result is claimed yet.

## What we learned
- Writing the rules down first (steering, EARS, properties) made decisions cheap.
- A model id copied from memory is a bug waiting to happen; check the docs.
- More lessons go here as the Log grows.

## What's next
Engine core and seeded dice, story loader, offline narrator, renderer, Telnet and
web transport, combat, carrier drop, the Bedrock/Gemini narrator chain, the AWS deploy, demo video.
Plan and dates: [`tasks.md`](.kiro/specs/telnet-tales/tasks.md).

## Kiro Workflow
| Feature | Use |
|---|---|
| Specs | requirements (EARS), design, tasks with requirement refs and a verify command |
| Steering | always-on product, tech, structure, golden rule, code style, retro terminal, testing, git, devlog; `fileMatch` for `engine/**` |
| Hooks | `run-tests-on-save` (ruff fix + pytest), `validate-story-graph`, format and file length, no nested loops, engine test reminder, `.kiro` guard, task gate (`make check`), `devlog-reminder` |
| Strategy | vertical slice first (engine, offline narrator, renderer, Telnet), LLM after |
| Property tests | P1-P17 in design.md; every engine change needs a hypothesis test |
| Kiro Crew | The user works with Mate (a Kiro Crew bot) and its workers. Their key requests, decisions and corrections are logged as `[crew]` entries in the Log. |

### Collaboration log
Convention: entries tagged `[crew]` record what the user asked or decided, what the
crew bot and workers did, corrections the user made, and what changed in the project.
Brief, no secrets, no raw chat dumps. Rules: [`devlog.md`](.kiro/steering/devlog.md).

## Log
Newest first.

### 2026-11-27 - [crew] Story loader and validator (task 3)
**What happened:** a Kiro Crew worker added stories/schema.py (StoryFile, status draft or final), loader.py (YAML load, all errors listed together) and graph.py (unknown ids, dead ends, unreachable nodes, nodes that cannot reach an ending, items required but nowhere to be found, item-aware winnability). Same vocabulary as scripts/validate_story_graph.py. No hypothesis failure found (P6 passes).
**Why it matters:** a bad story is refused with every error at once, before a player meets it.
**What we learned:** the nested-loop rule pushed the graph code into small helpers (exit_pairs, edge_pairs); it also made the code easier to read.

### 2026-11-27 - [crew] Actions and rules (task 2)
**What happened:** a Kiro Crew worker added ProposedAction with a closed allow-list, typed rejections, and pure rules for move, look, take and inventory. Story data models (Exit, Requirement, Encounter, StoryNode, Story) live in engine/story_models.py so rules do not import stories. No hypothesis failure found (P2, P3, P4, P5, P7 pass).
**Why it matters:** rejected actions provably leave the state equal, and unknown action types never apply.
**What we learned:** the story models belong to engine because dependencies point from stories to engine; stories/schema.py will re-export them.

### 2026-11-27 - [crew] Smoke deploy on AWS (S1)
**What happened:** a Kiro Crew worker built `infra/template.yaml` (SAM) and deployed it to the
user's account: a hello-world Lambda behind `POST /api/command`, a DynamoDB table, a private
S3 bucket and CloudFront. Through CloudFront the Lambda wrote one item and read it back.
Measured: 1.36 s for the first call (Lambda cold start, 369 ms init), then 0.81 s and
0.53 s warm; the Lambda itself takes 20 ms warm, the rest is the network and TLS.
**Why it matters:** the serverless path works, so the Lightsail fallback is not needed so far.
**What we learned:** `sam` hung once on this machine until telemetry was turned off. A security
rule blocks the agent from copying files to S3, so the user uploads `index.html` by hand.

### 2026-11-27 - [crew] User picks serverless AWS and fixes four decisions
**What happened:** the user and the crew bot compared Cloud Run, a Lightsail instance and
serverless AWS. The user chose serverless AWS and fixed four technical decisions: (1) an
HTTP API with `POST /api/command` instead of WebSockets, with baud pacing painted by the
browser; (2) one DynamoDB table for saves, an exact daily LLM counter and login lockout;
(3) a plain uv-built `.zip` with one SAM template; (4) real Telnet stays local, with a
byte-parity test against the Lambda handler. Bedrock is the primary LLM, Gemini the
fallback, offline last. A Kiro Crew worker rewrote ADR 0006, 0007, 0009, new ADR 0010,
R4/R6/R7/R10/R13, the design (new `design-aws.md`), the tasks and the checklists.
**Why it matters:** Kiro is an AWS product and the user has AWS credits. There is no
hackathon bonus for using AWS, so this is a story choice, not a score choice. It also
removes the old Cloud Run caveat: the daily counter no longer resets on restart.
**What we learned:** a turn-based game does not need a live connection. Plan: smoke deploy
on Sat 28 Nov; if serverless fails by Sun 29 Nov, fall back to Lightsail.

### 2026-11-26 - Engine core: models and seeded dice
**What happened:** `Stats`, `Player` and `GameState` are frozen Pydantic models that reject
bad values (stat over 5, more than 8 items, hit points above max). `roll_d20` and `check`
take a state and return the next one; the seed plus a draw count rebuild the dice, so a
saved game continues the same rolls. Tests: unit tests plus hypothesis for P1 (range and
rule) and P2 (same seed, same result, also after save and reload). No counterexample found.
**Why it matters:** every later rule can be replayed and tested from a seed.
**What we learned:** rebuilding the generator by replaying draws is simple but linear; fine
for a 40-turn call, noted as a shortcut in the code.

### 2026-11-26 - [crew] User pushes SaveStore and GEMINI_MODEL
**What happened:** the user asked for two spec changes and for crew work to be logged here.
(1) The model id is read only from `GEMINI_MODEL`, and must be checked with the real key
(`client.models.list()`, `list_models` command); an earlier worker had called
`gemini-3.5-flash-lite` current and `gemini-2.5-flash` deprecated, while the user believes
`gemini-2.5-flash-lite` is the standard light id. Neither is verified, so ADR 0006 now says so.
(2) Saves go through a `SaveStore` Protocol with a local store and an optional GCS store
([ADR 0009](docs/adr/0009-save-store.md)), because Cloud Run disk is ephemeral. A Kiro
Crew worker made the edits (R4.8-R4.10, R10.4-R10.6, P17, tasks 11.1, 13.1, 14.11, 14.12).
**Why it matters:** a judge returning the next day would lose a carrier-drop save without a bucket.
**What we learned:** a model id from any source, even a worker, is unverified until the key says so.

### 2026-11-26 - [crew] Earlier decisions by the user
**What happened:** reconstructed from the repo history, not from chat logs. The user defined
the architecture and style rules (golden rule, 200-line files, no nested loops, Spanish
comments), chose the Resurrection category, picked Gemini, a web demo with a login and
Cloud Run, and asked for the `run-tests-on-save` and `validate-story-graph` hooks. A crew
worker wrote the files; the user kept the decisions.
**Why it matters:** shows which choices were human and which were drafted by the agent.
**What we learned:** the user decides, the crew drafts and checks.

### 2026-11-26 - Spec aligned: Cloud Run, shared pipeline, Gemini narrator
**What happened:** design, requirements and tasks now cover Cloud Run deployment with a
BBS login (constant-time check, backoff), call caps with offline fallback, and one
render pipeline under both transports (new properties P14-P16). A docs check
claimed `gemini-2.5-flash` is deprecated; that is unconfirmed (see the `[crew]` entry above).
**Why it matters:** strangers cannot spend the credit, and web and Telnet cannot drift apart.
**What we learned:** verify model ids against the docs on the day you pick them.

### 2026-11-26 - Decisions: Gemini and Cloud Run
**What happened:** ADR 0006 (Gemini as default provider, optional Vertex AI) and ADR 0007
(web-only public demo on Cloud Run, max-instances 1, login gate, daily cap).
**Why it matters:** the team has a Gemini key and GCP credits; Cloud Run has no raw TCP,
so real Telnet is shown locally and in the video.
**What we learned:** a hosting limit shaped a product decision early.

### 2026-11-26 - Story graph validator and hooks
**What happened:** `scripts/validate_story_graph.py` checks unknown `target_id`, dead
ends, lines over 80 columns and unreachable nodes. Hooks `run-tests-on-save` and
`validate-story-graph` run it and the tests on save.
**Why it matters:** story errors fail at save time, before a player finds them.
**What we learned:** one shared vocabulary (`target_id`, `is_ending`) avoids drift.

### 2026-11-26 - Spec written
**What happened:** EARS requirements R1-R13, design with 13 properties, day-by-day tasks
(target: feature complete Tue 1 Dec).
**Why it matters:** each task cites requirements and a verify command.
**What we learned:** small rules fit the 4-day build window.

### 2026-11-26 - Steering files
**What happened:** always-on steering for product, tech, structure, golden rule, code
style (200-line files, no nested loops, Spanish comments), retro terminal, testing, git.
**Why it matters:** any agent follows the same rules.
**What we learned:** hard limits are only useful when a script enforces them.

### 2026-11-26 - Project bootstrap
**What happened:** repo, uv project, MIT license, Makefile (`make check`), checker scripts
with tests, `.kiro/` committed and guarded against `.gitignore`.
**Why it matters:** the hackathon requires `.kiro/` in the public repo.
**What we learned:** guard the rule with a hook, not with memory.

# DEVLOG archive 01

Oldest Log entries, moved from [`DEVLOG.md`](../../DEVLOG.md) (newest first).

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

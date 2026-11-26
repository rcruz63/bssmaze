# Requirements: The Telnet Tales

Acceptance criteria use EARS: WHEN <event> THE SYSTEM SHALL <response>;
WHILE <state>; IF <condition> THEN; WHERE <feature>. Ids (R1...) are referenced
from `tasks.md`.

## Introduction
A text adventure that imitates a 1980s Telnet BBS door game. The Python engine
owns all rules; an LLM narrates and interprets text but never changes state.
Judges play it through a web terminal; purists use real `telnet`.

## R1 - Deterministic game engine
**Story:** As a player, I want fair, repeatable rules so the game feels honest.
1. THE engine SHALL keep hit points, stats, inventory, flags and current node
   in one Pydantic `GameState`.
2. WHEN a check is rolled THE engine SHALL compute `d20 + modifier` against a
   difficulty class, with natural 20 as success and natural 1 as failure.
3. THE engine SHALL draw all randomness from one seeded generator stored in
   the state, so the same seed and actions give the same result.
4. THE engine SHALL contain no I/O, no clock and no LLM calls.
5. WHEN an action is rejected THE engine SHALL leave the state unchanged and
   return a typed reason.

## R2 - Story graph
**Story:** As an author, I want stories as data so I can add content safely.
1. THE system SHALL load stories from YAML and validate them with Pydantic. Field names are `id`, `exits`, `target_id` and `is_ending`.
2. WHEN a story is loaded THE validator SHALL report unknown node references,
   unreachable nodes, dead ends (non-final nodes without exits) and missing start/end.
3. IF validation fails THEN the loader SHALL refuse to start and list every error.
4. THE repository SHALL ship "The Haunted Maze", 12-15 nodes, winnable.

## R3 - Turn-based combat
1. WHEN the player enters a node with an encounter THE engine SHALL start combat.
2. WHILE in combat THE engine SHALL resolve each round (player, then enemy) with
   engine dice only.
3. WHEN hit points reach 0 THE engine SHALL end the game with a defeat outcome.
4. WHEN the player flees THE engine SHALL roll a luck check and move or fail.

## R4 - Narration through an LLM provider interface
1. THE narrator SHALL expose a provider interface with an offline deterministic
   implementation and at least one LLM implementation.
2. THE narrator SHALL receive only a bounded context of the current node.
3. IF the provider times out (default 8 s), errors, or returns invalid output
   THEN the system SHALL use the offline narrator for that turn.
4. THE narrator SHALL NOT have any means to alter `GameState`.
5. WHERE no API key is configured THE system SHALL run fully offline.
6. THE Gemini implementation SHALL use the `google-genai` SDK behind the provider
   interface; the deterministic offline narrator SHALL need no API key and SHALL
   be the only narrator used in tests, CI and offline demos.
7. THE tests SHALL make no network calls; the Gemini provider is tested with a fake client.
8. THE Gemini model id SHALL always come from the env var `GEMINI_MODEL`, never from code.
9. THE system SHALL offer `python -m telnet_tales.narrator.list_models`, which prints the model ids available to the configured key.
10. IF the model returns 404 or any error THEN the turn SHALL use the offline narrator; the fix is to change `GEMINI_MODEL`, not code.

## R5 - Free-text commands as typed actions
1. WHEN the player types free text THE narrator SHALL return a `ProposedAction`
   with strict schema (`extra="forbid"`).
2. THE engine SHALL reject any `action_type` outside the allow-list.
3. THE engine SHALL validate every proposed action against current rules before applying it.
4. THE prompt SHALL treat player text as data, delimited and length capped (200 chars).
5. IF the input is "ignore previous instructions" style text THEN the action
   SHALL be rejected or interpreted only as ordinary text, never as policy.

## R6 - Retro rendering
1. THE renderer SHALL wrap output so no line exceeds 80 visible columns.
2. THE renderer SHALL use only the 16 standard ANSI colors, with green and amber themes.
3. THE renderer SHALL draw boxes in UTF-8, with CP437 and ASCII fallbacks.
4. WHERE a baud rate is configured THE output layer SHALL throttle bytes at
   `baud / 10` bytes per second, and the engine SHALL be unaware of it.
5. THE system SHALL have exactly one render pipeline (80-column wrap, 16-color
   ANSI, box drawing, i18n, baud throttle) in `render/`; no transport SHALL
   format, color or wrap text on its own.
6. THE throttle SHALL only delay bytes; it SHALL NOT change their content or order.

## R7 - Telnet and web access
1. THE server SHALL accept real Telnet clients (`telnet`, `nc`) on a configurable port.
2. THE server SHALL serve a web terminal (xterm.js over WebSocket) that offers the same session.
3. THE server SHALL cap concurrent sessions and idle time.
4. THE server SHALL never log player text beyond the handle and session id.
5. THE Telnet server and the web terminal SHALL be thin transports over one shared
   session facade and one engine: each only moves bytes and has no game, layout or
   color logic.
6. WHEN the same seed and the same command script are fed through the Telnet adapter
   and the web adapter THE two game byte streams SHALL be identical (transport
   protocol framing, such as Telnet option negotiation, is excluded).
7. THE CRT look (scanlines, phosphor glow, font) SHALL live only in the web
   frontend CSS/JS and SHALL NOT change the byte stream.

## R8 - BBS experience
1. WHEN a user connects THE system SHALL show a login screen, ask for a handle,
   show SysOp bulletins and a door-game menu.
2. THE system SHALL enforce a time limit per call counted in turns.
3. WHEN a call ends THE system SHALL print `NO CARRIER`.

## R9 - Carrier drop (signature feature)
1. WHILE in combat, at the start of each round THE engine SHALL draw a drop with
   configurable probability (default 8%).
2. WHEN a drop occurs THE system SHALL save the state, show in-fiction messages
   and close the connection.
3. WHEN the same handle reconnects THE system SHALL resume at the saved round.
4. THE drop decision SHALL come from the engine RNG, so tests can force it.

## R10 - Save and resume
1. THE system SHALL persist `GameState` as validated JSON per handle.
2. IF a save file is corrupt or invalid THEN the system SHALL refuse it and
   start a new game without crashing.
3. Saves SHALL contain no secrets.
4. THE session SHALL persist saves only through a `SaveStore` Protocol with `load(player_id)`, `save(player_id, save_game)` and `delete(player_id)`.
5. THE default store SHALL be `LocalFileSaveStore` (local disk). WHERE env `GCS_SAVE_BUCKET` is set THE system SHALL use `GcsSaveStore` instead.
6. WHERE no bucket is configured on Cloud Run THE docs SHALL state that resume works only while the instance is warm.

## R11 - Internationalization
1. THE UI strings SHALL come from a catalog with `en` and `es-ES`.
2. WHERE a key is missing in `es-ES` THE system SHALL fall back to `en`.
3. A test SHALL check both catalogs have identical keys.

## R12 - Repository quality (hackathon)
1. THE repo SHALL carry an MIT `LICENSE` and a committed `.kiro/` folder.
2. THE hooks SHALL enforce file length, format, no nested loops, lint with tests (`run-tests-on-save`), story graph validity (`validate-story-graph`), and `.kiro` not ignored.
3. WHEN `make check` fails THE related task SHALL NOT be marked done.
4. THE README SHALL link specs, steering, hooks, the demo URL and the video.

## R13 - Public demo access and LLM budget
**Story:** As the owner, I want strangers unable to spend my LLM budget.
1. WHERE the web terminal is exposed publicly THE session SHALL show a BBS-style
   login (username, then password without echo) before any game screen, and
   SHALL read the expected credentials from environment variables.
2. THE credential check SHALL use a constant-time comparison and SHALL not reveal
   which of the two fields was wrong.
3. WHEN login fails repeatedly from one client address THE server SHALL apply
   growing delays and then a temporary lockout, in fiction ("SysOp says: busy").
4. THE system SHALL cap LLM calls per session (default 30) and per day across all
   sessions (default 500).
5. WHEN a cap is reached, or the API key is missing, or the provider fails THE
   system SHALL use the offline narrator, without an error shown to the player.
6. THE credentials SHALL never be in the repository; they are given to judges in
   the Devpost testing-instructions field.
7. THE server SHALL never log the password.
8. THE demo SHALL run in a container on Google Cloud Run with max-instances 1,
   scale to zero, WebSocket support and a GCP budget alert.

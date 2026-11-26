---
inclusion: always
---

# Product: The Telnet Tales

**Tagline:** Summoning the ghost of 1980s dial-up BBS doors to run AI-powered
interactive fiction. Connect at 2400 baud, explore ASCII labyrinths, and pray
the SysOp doesn't drop your carrier mid-combat.

## What it is
A conversational text adventure that imitates a Telnet BBS "door game". The
player dials in, picks a handle, reads SysOp bulletins and enters a door game
menu. The adventure ("The Haunted Maze") is a graph of story nodes. An LLM
narrates and interprets free text, but the Python engine owns every rule.

## Hackathon context
- Kiroween 2026, category **Resurrection**. Build window: 30 Oct - 4 Dec 2026.
- Judges score five equal criteria: Potential Impact, Technological
  Implementation (depth and variety of Kiro use), Design, Innovation,
  Presentation.
- Judges can only test through a URL: ship a web terminal next to real Telnet.
- Game language is **English**. Dev/debug UI strings also support `es-ES`.

## Signature feature
**Carrier drop:** the SysOp may randomly cut the connection mid-combat. The
event is decided by the engine, the state is saved, and reconnecting resumes
the fight with in-fiction messages ("NO CARRIER").

## Non-goals
Multiplayer, accounts with passwords, payments, graphical clients.

## Pointers
- Rules of play: #[[file:docs/game-design.es.md]]
- Spec: #[[file:.kiro/specs/telnet-tales/requirements.md]]

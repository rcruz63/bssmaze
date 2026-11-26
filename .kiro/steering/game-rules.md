---
inclusion: always
---

# Game rules (summary; full text in docs/game-design.es.md)

- **Stats:** `hit_points` (max 20), `wits`, `brawn`, `luck` (each 0..5 as a
  modifier), plus an inventory of at most 8 item ids.
- **Check:** `d20 + modifier >= difficulty_class`. Natural 20 always succeeds,
  natural 1 always fails.
- **RNG:** one seeded `random.Random` owned by `GameState` (seed + draw count
  are stored). Same seed + same actions = same game, replayable.
- **Story:** nodes with exits, requirements (item or stat), items, encounters.
  Loaded from YAML, validated by Pydantic plus a graph validator (reachability,
  dead ends, unknown references).
- **Combat:** turn based, engine only. Player picks `attack`, `use` or `flee`;
  the engine rolls for both sides. The LLM may only color the text.
- **Carrier drop:** at the start of each combat round the engine draws
  `drop_chance` (default 8%). On a drop the state is saved, the player sees
  `NO CARRIER`, and reconnecting resumes the same round.
- **Call time limit:** each call lasts N turns (default 40), counted in turns,
  not wall clock, so tests are deterministic.
- **Allowed action types:** move, look, take, use, attack, flee, inventory,
  help, quit. Anything else is rejected with an in-fiction message.

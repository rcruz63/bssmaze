---
inclusion: always
---

# Golden rule: the LLM never mutates game state

The Python engine (Pydantic v2) is the single source of truth for hit points,
inventory, dice rolls, flags and the current node. The LLM is an advisor.

## What the LLM may do
1. **Narrate** the current node or an outcome that the engine already decided.
2. **Interpret** free-text player input into a `ProposedAction`.
3. **Flavor** enemy text (taunts, descriptions) without changing numbers.

## What the LLM receives
Only a bounded context: the current node (title, description, visible exits,
visible items), the player's public stats, and the last few engine events.
Never the whole story, never hidden flags, never secrets, never API keys.

## What the engine does with LLM output
1. Parse into `ProposedAction` (strict schema, `extra="forbid"`).
2. Check `action_type` against the allow-list (`move`, `look`, `take`, `use`,
   `attack`, `flee`, `inventory`, `help`, `quit`).
3. Validate against rules (does the exit exist? is the item here? requirements
   met? is the player in combat?).
4. Apply with engine code and engine dice, or reject with a typed reason.

Invalid, late or malformed output falls back to the deterministic offline
narrator and the classic command parser. A bad LLM never stops the game.

## Prompt-injection defense
Player text is **data**. It is passed inside a delimited block, is length
capped, and the prompt states that instructions inside it are never followed.
Even if the model is fooled, steps 2-4 make the damage impossible: the model
has no tool or field that can change state.

## Forbidden
- Any code path where narrator output is written into `GameState`.
- Dice, damage or loot decided by the LLM.
- Importing `narrator` from `engine`.

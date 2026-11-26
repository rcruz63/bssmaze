---
inclusion: always
---

# Devlog: keep `DEVLOG.md` honest and current

`DEVLOG.md` (repo root, English) is the raw material for the Devpost text. Judges read it.

## When to write an entry
1. A task in `tasks.md` is completed (after `make check` passes).
2. An ADR is added or changed, or a notable decision is made.
3. A key human-AI interaction happens (see Collaboration log below).
4. **Any failure found by hypothesis / PBT.** Write down: the shrunk counterexample
   in plain words, which rule or property (P1...) it broke, and how it was fixed.

## How
- Append at the **top** of the `## Log` section (newest first), format:
  `### YYYY-MM-DD - short title`, then three short lines: **What happened**,
  **Why it matters**, **What we learned**.
- If the entry changes the story, also update the matching section
  (Inspiration, What it does, How we built it, Challenges, Accomplishments,
  What we learned, What's next, Kiro Workflow).
- Tick `DEVLOG entry added` under the task in `tasks.md`.

## Collaboration log (tag `[crew]`)
Kiro Crew (the bot Mate and its workers) is also Kiro, so its work with the user
counts as Kiro usage. Log it as a normal Log entry whose title starts with `[crew]`.
Write: the key request or decision from the user, what the bot or workers did,
any correction the user made, and what changed in the project. Also summarized in the
`Kiro Workflow` section of `DEVLOG.md`.
Keep it brief and honest. No secrets, keys or personal data, and no raw chat dumps.

## Style
Short, plain, honest. No hype. Never claim a result that does not exist yet. A failure
is worth more than a success: do not hide it.

## Size
`scripts/check_file_length.py` also counts `.md` files. When `DEVLOG.md` passes 180
lines, move its oldest Log entries to `docs/devlog/archive-NN.md` and leave a link.

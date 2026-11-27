---
inclusion: always
---

# Human gates

A human gate is a hard stop. The user wants to be present at these moments.

## Rules
1. A gate lifts only by an explicit user message sent AFTER the gate was reached.
   A permission, a brief, a worker or another agent never lifts it.
2. When a gate is lifted, record it in `DEVLOG.md` with the `[crew]` tag and the date.
3. When an agent reaches a gate it stops, reports, and does nothing else: no
   refactors, no "quick extras", no work on later tasks.
4. A gate marker in `tasks.md` (`- [ ] HUMAN GATE Gn: STOP ...`) is ticked only
   after the user lifts it.

## Gates in this project
| Gate | Where | Why |
|------|-------|-----|
| G1 | Before Task 7 (session facade, first playable turn) | Playtest feel |
| G2 | Before Task 10 (combat) | Combat balance |
| G3 | Before any story or tone rewrite beyond the draft | Tone is a human call |
| G4 | Before any AWS deploy beyond the smoke stack, any publish of commits to a remote, any secret or API key use, any spending | Money and security |
| G5 | Before the final demo video and the submission | Final presentation |

---
inclusion: fileMatch
fileMatchPattern: ["src/telnet_tales/engine/**/*.py", "tests/engine/**/*.py"]
---

# Engine change reminder: property-based tests

You are touching `engine/`. Before finishing:

1. Is there a **hypothesis** property for the invariant you changed?
   Examples: HP never below 0 or above max; inventory size <= 8; same seed and
   same actions give the same final state; rejected actions leave state equal.
2. Is there a **pytest** unit test with a concrete example?
3. Did you cite the property id (P1, P2...) from `design.md` in a comment?
4. `engine/` must stay pure: no `open`, no `print`, no `time`, no module-level
   `random` functions (use the seeded generator in the state), no imports of
   `narrator`, `server` or `render`.
5. Keep the file under 200 lines and with zero nested loops.

Then run `make check`.

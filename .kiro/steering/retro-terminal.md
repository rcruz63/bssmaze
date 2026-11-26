---
inclusion: always
---

# Retro terminal rules

All output is produced by `render/`. Game logic never writes escape codes.

## 80 columns
- Output lines are at most **80 visible columns**. The formatter word-wraps
  automatically and never lets text overflow. ANSI sequences do not count as
  visible columns. Words longer than a line are hard-split.
- A property test must hold: for any text and theme, every rendered line has
  `visible_width <= 80`.

## Color and themes
- Only the **standard 16 ANSI colors** (SGR 30-37, 90-97, reset 0, bold 1).
  No 256-color or truecolor.
- Two themes: **green** phosphor and **amber** phosphor. Themes map semantic
  roles (title, body, danger, system) to colors; code uses roles, not colors.

## Box drawing
- Default: UTF-8 box characters, compatible with `telnet`, `nc` and the web
  emulator.
- Fallback: CP437 mode and a pure ASCII mode (`+ - |`) selected per session
  (`TERM`, client negotiation or `/ascii` command). Widths stay identical.

## Baud throttle
- Simulated line speed is configurable (2400, 9600, ... or 0 = unlimited).
- Throttling lives **only in the output layer** (`render/throttle.py` and the
  server writer). It sleeps between bytes (10 bits per byte on a serial
  line). The engine and narrator never know about baud rate.
- Tests inject a fake clock; they never really sleep.

## BBS flavor
Login screen, handle prompt, SysOp bulletins, door menu, per-call time limit,
`NO CARRIER` on drop. Keep the tone affectionate and a bit spooky.

---
inclusion: always
---

# Git workflow

- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `test:`, `refactor:`,
  `chore:`, `ci:`. Imperative English subject, at most 72 characters.
- **Small commits:** one task from `tasks.md` per commit, with the task number
  in the body. Never mix refactor and feature.
- Run `make check` before committing. Do not commit with failing checks.
- **Never commit secrets:** `.env`, API keys, tokens, save files. Only
  `.env.example` with empty values. If a secret leaks, rotate it first.
- **Never add `.kiro` or any subfolder to `.gitignore`.** The hackathon requires
  `.kiro/` in the public repository. `scripts/check_gitignore_kiro.py` guards it.
- Do not push to `main` without being asked; do not force-push.
- All code must be written inside the hackathon window (30 Oct - 4 Dec 2026).
  Do not paste pre-existing code; disclose anything third-party in the README.

---
inclusion: manual
---

# Kiroween 2026 submission checklist (use with `#submission-checklist`)

## Required
- [ ] Public GitHub repo with OSI license (`LICENSE`, MIT) visible in the About box.
- [ ] `.kiro/` committed with steering, specs and hooks. `git check-ignore -v .kiro` prints nothing.
- [ ] Built within 30 Oct - 4 Dec 2026; no pre-existing code (README states it).
- [ ] Category selected: **Resurrection**.
- [ ] Working URL for judges (CloudFront web terminal) plus Telnet instructions. The offline narrator works with no AWS or Gemini access.
- [ ] Demo credentials (web terminal login) in the Devpost **testing instructions** field only, never in the repo or README. Telnet shown locally/video (the deployment has no raw TCP).
- [ ] State: `STATE_TABLE_NAME` set in the Lambda; a carrier-drop save resumes after a day (DynamoDB, TTL).
- [ ] `BEDROCK_MODEL_ID` (and `GEMINI_MODEL` if used) set and checked with `list_models` on the real account and key; Bedrock model access enabled in the region.
- [ ] Serverless AWS deployed with `sam deploy`; AWS Budgets alert set; daily LLM cap checked.
- [ ] Demo video under 3 minutes on YouTube (public or unlisted), no copyrighted music.
- [ ] Text description: pitch, how Kiro was used (specs, steering, hooks, strategy, experiments), what was built.
- [ ] README: quickstart, architecture diagram, screenshots, link to `.kiro/` artifacts.

## Bonus prizes
- [ ] Blog post (dev.to / Medium / Hashnode) about building with Kiro; link in submission.
- [ ] Social post with **#KiroweenHackathon26**; link in submission.

## Final pass
- [ ] `make check` green on a fresh clone (`uv sync`).
- [ ] No secrets in history.
- [ ] Submit before the 4 Dec 2026 deadline, not at the last minute.
